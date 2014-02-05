/*
 * p.cpp
 *
 *  Created on: 4 Feb 2014
 *      Author: carl
 */
#include <iostream>
#include <cmath>

using namespace std;

#define R 6371
#define sqr(x) ((x) * (x))

int main()
{
	int n;
	cin >> n;

	double x, y, z;
	double sx, sy, sz;
	double distance = 0;
	for (int i = 0; i <= n; i++)
	{
		double ox = x, oy = y, oz = z;
		double lat, lon;
		if (i < n) {
			cin >> lat >> lon;

			lat = lat * 2 * M_PI / 360;
			lon = lon * 2 * M_PI / 360;

			x = cos(lon) * cos(lat) * R;
			y =            sin(lat) * R;
			z = sin(lon) * cos(lat) * R;
		}
		else {
			x = sx; y = sy; z = sz;
		}

		if (i == 0)
		{
			sx = x; sy = y; sz = z;
			continue;
		}

		double c = sqrt(sqr(x-ox) + sqr(y-oy) + sqr(z-oz));

		double angle = acos((2 * R * R - sqr(c)) / (2 * R * R));

		distance += angle * R;
	}

	cout.precision(6);
	cout.setf(ios::fixed, ios::floatfield);
	cout << distance << endl;

	return 0;
}
