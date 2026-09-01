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
export type TaskKind = 'message' | 'audio';
export type TaskStatus = 'running' | 'done' | 'failed';
export interface TaskEvent {
    /** Monotonic per-task sequence, so a reconnecting client can skip what it saw. */
    seq: number;
    data: unknown;
}
interface Task {
    id: string;
    projectId: string;
    kind: TaskKind;
    status: TaskStatus;
    events: TaskEvent[];
    subscribers: Set<(e: TaskEvent) => void>;
    error?: string;
    startedAt: number;
    endedAt?: number;
}
/** Emit handle handed to a task runner — it just calls emit(data). */
export interface TaskEmitter {
    taskId: string;
    emit: (data: unknown) => void;
}
export declare class TaskRegistry {
    private tasks;
    private seq;
    private idCounter;
    /** Tasks completed > this long ago are pruned on the next create(). */
    private static readonly TTL_MS;
    /**
     * Start a detached task. `runner` receives an emitter; whatever it emits is
     * fanned out to current subscribers AND retained for replay. The runner's
     * resolved value is ignored (state lives in emitted events + the project);
     * a thrown error marks the task failed and is emitted as a final event.
     */
    create(projectId: string, kind: TaskKind, runner: (emitter: TaskEmitter) => Promise<void>): string;
    /** The newest still-running (or just-finished) task for a project, if any. */
    activeTaskFor(projectId: string): {
        id: string;
        kind: TaskKind;
        status: TaskStatus;
    } | null;
    /**
     * Subscribe to a task: immediately replays events after `sinceSeq`, then calls
     * `onEvent` for each new one. Returns an unsubscribe fn, plus whether the task
     * is already finished (so the caller can close the stream). `null` = no such task.
     */
    subscribe(taskId: string, sinceSeq: number, onEvent: (e: TaskEvent) => void): {
        unsubscribe: () => void;
        finished: boolean;
    } | null;
    get(taskId: string): Task | undefined;
    private prune;
}
export {};
//# sourceMappingURL=task-registry.d.ts.map