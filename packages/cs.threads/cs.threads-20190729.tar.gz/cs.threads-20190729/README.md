threading and communication/synchronisation conveniences


Thread related convenience classes and functions.

## Class `AdjustableSemaphore`

A semaphore whose value may be tuned after instantiation.

## Function `bg(func, daemon=None, name=None, no_start=False, no_logexc=False)`

Dispatch the callable `func` in its own Thread; return the Thread.

Parameters:
* `func`: callable to run in its own `Thread`.
* `daemon`: optional argument specifying the .daemon attribute.
* `name`: optional argument specifying the Thread name.
* `no_start`: optional argument, default `False`.
  If true, do not start the `Thread`.
* `no_logexc`: if false (default `False`), wrap `func` in `@logexc`.

## Class `LockableMixin`

Trite mixin to control access to an object via its ._lock attribute.
Exposes the ._lock as the property .lock.
Presents a context manager interface for obtaining an object's lock.

## Function `locked(func)`

A decorator for monitor functions that must run within a lock.
Relies upon a ._lock attribute for locking.

## Function `locked_property(func, lock_name='_lock', prop_name=None, unset_object=None)`

A thread safe property whose value is cached.
The lock is taken if the value needs to computed.

## Function `via(cmanager, func, *a, **kw)`

Return a callable that calls the supplied `func` inside a
with statement using the context manager `cmanager`.
This intended use case is aimed at deferred function calls.

## Class `WorkerThreadPool`

MRO: `cs.resources.MultiOpenMixin`, `cs.obj.O`  
A pool of worker threads to run functions.

### Method `WorkerThreadPool.__init__(self, name=None, max_spare=4)`

Initialise the WorkerThreadPool.

Paramaters:
`name`: optional name for the pool
`max_spare`: maximum size of each idle pool (daemon and non-daemon)

## Class `WTPoolEntry`

MRO: `builtins.tuple`  
WTPoolEntry(thread, queue)
