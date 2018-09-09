#include <iostream>
#include <unistd.h>

int main() {
	for (int i = 0; i < 5; ++i) {
		std::cout << i << std::endl;
		sleep(1);
	}
}