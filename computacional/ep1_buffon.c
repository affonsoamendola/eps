//Computational Astronomy
//EP 1 - Buffon's Needle
//By Affonso Amendola

//Code licensed under GPLv3, available on my github.
//https://github.com/affonsoamendola/eps/tree/master/computacional

//So Alex, I chose to do it in C, despite the many issues with rand() and srand()
//mainly because of the speed, I'd be really curious to see the differences between
//my version and a Python version, unfortunately due to my legendary lazyness, I
//left this work to the absolute last available time, and I dont have time to do
//a different version just to appease my curiosity.

//I really need to get my s*** together.

#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <math.h>

const double strip_size_x = 4.0;
const int number_of_strips = 1;

const double field_size_x = strip_size_x * number_of_strips;
const double field_size_y = 100.0;

const double needle_length = 4.0;

double get_random()
{
	//There's a great talk on why rand()%value is crap, 
	//but in this case I believe this returns a uniform distribution, if rand()
	//is uniform.

	//https://channel9.msdn.com/Events/GoingNative/2013/rand-Considered-Harmful
	return (double)rand()/(double)RAND_MAX;
}

//Since this is C, you cant return 2 values like in modern languages,
//a common solution to that is using pointer arguments to move values outside of
//the scope.
void get_random_position(double* x_out, double* y_out, double max_x, double max_y)
{
	double x;
	double y;

	x = get_random() * max_x;
	y = get_random() * max_y;

	*x_out = x;
	*y_out = y;
}

int crossing_boards(double x, double footprint)
{
	//This puts all of the needles on the same strip, since all of them are equal
	//this makes the math simpler
	while(x - strip_size_x >= 0.0) x -= strip_size_x;

	double half_footprint = footprint/2.0;

	if(x + half_footprint >= strip_size_x || x - half_footprint < 0.0)
	{
		return 1;
	}
	else
	{
		return 0;
	}
}

void buffon_experiment(int number_of_needles)
{
	clock_t begin = clock();
	int crossed = 0;

	for(int i = 0; i < number_of_needles; i++)
	{
		double needle_x;
		double needle_y;
		double needle_angle;

		get_random_position(&needle_x, &needle_y, field_size_x, field_size_y);

		//I believe it is not nescessary to simulate all angle quadrants of needles, 
		//since they are all mirror versions of each other.
		needle_angle = get_random() * 90.0;

		double needle_footprint = cos(needle_angle * M_PI / 180.0) * needle_length;

		if(crossing_boards(needle_x, needle_footprint))
		{
			crossed += 1;
		}
	}

	double pi_approximation = (2.0 * needle_length * number_of_needles) / (strip_size_x * crossed);

	double real_error = fabs(pi_approximation - M_PI);
	double estimated_error = fabs(pi_approximation/sqrt(number_of_needles));

	clock_t end = clock();

	double time = (double)(end - begin) / CLOCKS_PER_SEC;

	printf("N=%d\n", number_of_needles);
	printf("PI=%f\n", pi_approximation);
	printf("Real_Error=%f\n", real_error);
	printf("estimated_error=%f\n", estimated_error);
	printf("Time=%f secs\n", time);
}

int main(int argc, char const *argv[])
{
	
	//So Alex,
	//
	//This is bad, time() returns the amount of seconds since jan 1, 1970, meaning
	//that running this software two times in the same second gets the same result
	//
	//Which isn't that unlikely, if for example this was running on multiple threads
	//And they were initialized on the same tick of the CPU, they would always
	//return the same values.
	//
	//But on C without depending on external libraries
	//(Or doing some magic to access the clock manually)
	//there's not much I can do.
	//
	//Should'nt really affect anything, since this iteration of the program runs
	//on a single thread, and there's really no reason to run it multiple times.
	srand((unsigned int)time(NULL));

	if(argc != 2)
	{
		printf("Usage: ep1_buffon number_of_needles\n");
		return -1;
	}
	//Executing the experiment with the 1st argument of the program as the number of 
	//needles.
	buffon_experiment(atoi(argv[1]));

 	/*
	for(int n = 500000; n < 10000000; n += 5000)
	{                     
		buffon_experiment(n);
	}
	*/
	return 0;
}

//Be Excellent to Each Other
//
//Made under the influence of my amazing 90s spotify playlist.
//https://open.spotify.com/playlist/1jAXK6e45VyFc7p5Myutg7?si=SgNQ0yV0SdO4hkLOOA1Awg