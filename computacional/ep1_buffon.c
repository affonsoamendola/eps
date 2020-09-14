//Computational Astronomy
//EP 1 - Buffon's Needle
//By Affonso Amendola

//Code licensed under GPLv3, available on my github.

//So Alex, I chose to do it in C, despite the many issues with rand() and srand()
//mainly because of the speed, I'd be really curious to see the differences between
//my version and a Python version, unfortunately due to my legendary lazyness, I
//left this work to the absolute last available time, and I dont have time to do
//a different version just to appease my curiosity.

//I really need to get my s*** together.

#include <stdlib.h>
#include <stdio.h>
#include <time.h>

const float strip_size_x = 4.0f;
const int number_of_strips = 100;

const float field_size_x = strip_size_x * number_of_strips;
const float field_size_y = 100.0f;

const float needle_size = 4.0f;

float get_random()
{
	//There's a great talk on why rand()%value is crap, 
	//but in this case I believe this returns a uniform distribution, if rand()
	//is uniform.

	//https://channel9.msdn.com/Events/GoingNative/2013/rand-Considered-Harmful
	return (float)rand()/(float)RAND_MAX;
}

//Since this is C, you cant return 2 values like in modern languages,
//a common solution to that is using pointer arguments to move values outside of
//the scope.
void get_random_position(float* x_out, float* y_out, float max_x, float max_y)
{
	float x;
	float y;

	x = get_random() * max_x;
	y = get_random() * max_y;

	*x_out = x;
	*y_out = y;
}

int main(int argc, char const *argv[])
{
	//So Alex,
	//
	//This is bad, time() returns the amount of seconds since jan 1, 1970, meaning
	//that running this software two times in the same second gets the same result
	//
	//Which isn't that unlikely.
	//
	//But on C without depending on external libraries 
	//(Or doing some magic to access the clock manually)
	//there's not much I can do.

	srand((unsigned int)time(NULL));

	float x;
	float y;

	get_random_position(&x, &y, 1000.0f, 1000.0f);

	printf("%f %f\n", x, y);

	return 0;
}