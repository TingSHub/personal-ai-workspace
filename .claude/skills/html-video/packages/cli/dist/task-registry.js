/**
 * In-process registry of long-running generation tasks (video frames, audio).
 *
 * The point: a generation must NOT die when the browser navigates away or the
 * SSE connection drops. Previously each generate endpoint streamed straight to
 * the request's `res`; closing it (switching project / refresh) killed the run.
 *
 * Now a task runs detached from any request. It accumulates its events, so a
 * client can (re)subscribe at any time and get a full replay + live tail. The
 * runner's promise drives the work; subscribers come and go freely.
 *
 * In-memory only — tasks live for the studio process lifetime. A server restart
 * loses in-flight tasks (acceptable: the studio is a local single-process tool).
 */
export class TaskRegistry {
    tasks = new Map();
    seq = 0;
    idCounter = 0;
    /** Tasks completed > this long ago are pruned on the next create(). */
    static TTL_MS = 10 * 60_000;
    /**
     * Start a detached task. `runner` receives an emitter; whatever it emits is
     * fanned out to current subscribers AND retained for replay. The runner's
     * resolved value is ignored (state lives in emitted events + the project);
     * a thrown error marks the task failed and is emitted as a final event.
     */
    create(projectId, kind, runner) {
        this.prune();
        const id = `task_${Date.now().toString(36)}_${(this.idCounter++).toString(36)}`;
        const task = {
            id,
            projectId,
            kind,
            status: 'running',
            events: [],
            subscribers: new Set(),
            startedAt: Date.now(),
        };
        this.tasks.set(id, task);
        const emit = (data) => {
            const ev = { seq: ++this.seq, data };
            task.events.push(ev);
            for (const fn of task.subscribers) {
                try {
                    fn(ev);
                }
                catch { /* a dead subscriber shouldn't break the task */ }
            }
        };
        // Run detached. Never rejects out of here.
        void runner({ taskId: id, emit })
            .then(() => {
            task.status = 'done';
            task.endedAt = Date.now();
            emit({ type: 'task_done' });
        })
            .catch((err) => {
            task.status = 'failed';
            task.error = err instanceof Error ? err.message : String(err);
            task.endedAt = Date.now();
            emit({ type: 'task_failed', message: task.error });
        });
        return id;
    }
    /** The newest still-running (or just-finished) task for a project, if any. */
    activeTaskFor(projectId) {
        let newest = null;
        for (const t of this.tasks.values()) {
            if (t.projectId !== projectId)
                continue;
            if (!newest || t.startedAt > newest.startedAt)
                newest = t;
        }
        if (!newest)
            return null;
        return { id: newest.id, kind: newest.kind, status: newest.status };
    }
    /**
     * Subscribe to a task: immediately replays events after `sinceSeq`, then calls
     * `onEvent` for each new one. Returns an unsubscribe fn, plus whether the task
     * is already finished (so the caller can close the stream). `null` = no such task.
     */
    subscribe(taskId, sinceSeq, onEvent) {
        const task = this.tasks.get(taskId);
        if (!task)
            return null;
        for (const ev of task.events) {
            if (ev.seq > sinceSeq)
                onEvent(ev);
        }
        if (task.status !== 'running') {
            return { unsubscribe: () => { }, finished: true };
        }
        task.subscribers.add(onEvent);
        return {
            unsubscribe: () => { task.subscribers.delete(onEvent); },
            finished: false,
        };
    }
    get(taskId) {
        return this.tasks.get(taskId);
    }
    prune() {
        const now = Date.now();
        for (const [id, t] of this.tasks) {
            if (t.status !== 'running' && t.endedAt && now - t.endedAt > TaskRegistry.TTL_MS) {
                this.tasks.delete(id);
            }
        }
    }
}
//# sourceMappingURL=task-registry.js.map