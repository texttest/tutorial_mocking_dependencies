# Current Time using System

This python script uses the underlying system command 'date'. It only currently works on a unix system.

Below are instructions for a demo of how to test this with TextTest and capturemock.

1. Go to directory in shell. Run current_time_system.py. Say what it does and look at the code briefly: we're just repackaging "date"
2. texttest --new
3. Fill in form. Enable CaptureMock checkbox. Locate program.
4. Create test, run it, approve it. Point out that it fail a minute later. Point out that filtering isn't appropriate.
5. Select root suite, Definition Files, right click, Create/Import. Choose capturemockrc. Add the contents

[command line]
intercepts = date

Explain what this does: i.e. captures the behaviour of "date".

6. Run the test in record mode. Explain what has happened, look at the externalmocks file and explain the syntax.
7. Run in replay mode, point out test is green when time is different.

