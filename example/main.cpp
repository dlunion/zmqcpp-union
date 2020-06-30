

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