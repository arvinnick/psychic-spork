**Event loop**: consider this as a loop over your code, which will iterate and take the jobs to be done, some added by you and some by asyncio. This loop will constantly watch, take the jobs and execute them roughly in order. When there is nothing left, it rests. asyncio.run() makes an eventloop, adding the called function to it.  
**Thread**: a stream which is a part of a process with its stack space, register counter and program space. Each process has some threads. Threads within a process share the same memory space.  
In python, we can’t achieve true multithreading (just an illusion of it) because Python has a mechanism called GIL (global interpreter lock) which will prevent more than one thread to be executed on a time.  
**Multiprocessing** means making multiple processes.  
**Asyncio** is single threaded, single process. It uses cooperative multitasking which means tasks give up control voluntarily. For heavy computation we need processes instead.   
The awaitable object types in Python asyncio:

- **Coroutine**: objects created when you call an async function (async function is also called coroutine function). It represents the logic of the function and creating it, doesn’t automatically start the function.  
- **Tasks**: wrappers around coroutines that are scheduled on the event loop. In other words, when the event loop picks up a coroutine, it will become a task. They can be executed independently.  
  - We can make the task using create\_task. When we await the task, it will be handed over the event loop and get executed when it gets a chance.  
  - The task keep track of a series of callbacks.  
  - When we await a coroutine, we are creating the task and run it at the first time.  
  - The task might get garbaged collected and not going to the event loop. Therefore a call to the coroutine is better to be added to the eventloop, not the task.  
- **Futures**: low level objects representing the results. We don’t use the futures, but they are like promises in JScript.  
  - Features do not represent the computation itself; they represent the result and the state of that computation which might be pending, done or cancelled  
  - It’s actually the feature which stores the series of the callbacks, and the task holds it because it inherits from future class. 

In Python, we make the coroutine using the async keyword. After you use that keyword, you will make a coroutine. Calling that function will make a coroutine object which can be awaited.		  
**Await:** this keyword can be used in two ways: await coroutine and await task. “Await task” will cede the control from the current task or coroutine to the event loop.

- For the tasks, awaiting them adds their callback to the eventloop, then gives back the control to the eventloop. After that, later on, the eventloop will come back and takes the tasks callback to do whatever is there. This is not good, because going back on stack means a huge overhead.  
- For coroutines, awaiting will not handle the control back to the event loop. Awaiting a coroutine without wrapping it in a task is exactly like invoking a regular Python function.

Debugging:

- You can enable asyncio debug mode in asyncio.run by its argument. It will give you a lot of information. You can’t use cycling debugging (what you always do).

Under the hood:

- Asyncio uses coroutine.send to resume or start a coroutine. It gets an “arg” argument. If we are resuming it, the arg will be the return value of the yield statement which has originally paused it. Otherwise (if we are running the coroutine for the first time), it will be None.  
- **You had no idea so far what “yield” does so far**. Yield pauses the execution, remembers the state, gives the value to the state and after finishing the rest of the program, goes back to the stack and executes what comes after it (**this just ripped me apart**).  
- When you yield, it will go not just one level up in the call stack, but all the way to the main routine.  
- Awaiting a coroutine is just calling “\_\_await\_\_” method of its object. \_\_await\_\_ method should have a yield statement or else it will not cede control.