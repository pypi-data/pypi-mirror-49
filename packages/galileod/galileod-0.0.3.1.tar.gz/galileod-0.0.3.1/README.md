# Galileo-middleware
Repository holding python code for client-side Galileo functions

# Starting from Scratch
1. Clone the repo. I assume you put it resides in a directory called
   `Galileo-middleware` and that it is your working directory

2. Create a new Python virtualenv: `$ python3 -m venv venv`
3. Activate the virtualenv: `$ source venv/bin/activate`
4. Install the middleware and it's dependencies in one fell swoop: `$ pip3 install -e .`
5. When you're done don't forget to run `$ deactivate` to leave the virtualenv

# Invoking the middleware
* A script is automatically created at `venv/bin/galileod`. This is also
  automatically in your `PATH` if you've activated the `venv`.  So
  assuming you have activated the `venv` you can just run `galileod
  run`!

* `galileod --help` will show you options that control the
  construction of the Galileo object.
* `galileod run --help` shows you options pertaining to the flask
  server instance that will be created.

* So if I wanted to start the server on port 8089, and use a 20 second
  device polling period, I'd issue `galileod --devpoll 20 run --port
  8089`
