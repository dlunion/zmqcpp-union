# zmqcpp-union | [中文说明](README-cn.md)
* Merge all libzmq source code into one cpp/hpp file

## Startup

* Make zmq_u.cpp and zmq_u.hpp
```bash
python make_cpp_hpp.py  # to generate zmq_u.cpp and zmq_u.hpp
```

* cpp code
```cpp
#include "zmq_u.hpp"
#include <string>
#include <iostream>

using namespace std;

int main()
{
	zmq::context_t ctx;
	zmq::socket_t sock(ctx, zmq::socket_type::sub);
	sock.connect("tcp://192.168.27.248:5555");
	sock.set(zmq::sockopt::subscribe, "");

	zmq::message_t message;

	while (true) {
		auto r = sock.recv(message);
		cout << string((char*)message.data(), (char*)message.data() + message.size()) << endl;
	}
	return 0;
}
```


## Reference
* [libzmq](https://github.com/zeromq/libzmq)
* [zguide-cn](https://github.com/anjuke/zguide-cn)
* [cppzmq](https://github.com/zeromq/cppzmq)
