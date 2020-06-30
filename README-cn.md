# zmqcpp-union
* 合并zmq所有源代码为一个cpp和hpp文件，便于使用

## 开始使用

* 生成 zmq_u.cpp 和 zmq_u.hpp
```bash
python make_cpp_hpp.py
```

* 如果你使用新版本的zmq，依然可以使用make_cpp_hpp.py进行操作得到cpp和hpp
* 如果使用新版zmq，你需要先通过cmake得到windows下和linux下platform.h文件，然后合并为一个platform.h放到src下面即可。具体可以参考[platform.h](src.zmq4.3.2/platform.hpp)
* 生成的代码支持windows和linux系统
* C++代码，你将可以使用[zmq.h](https://github.com/zeromq/libzmq)和[zmq.hpp](https://github.com/zeromq/cppzmq)的所有特性
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
