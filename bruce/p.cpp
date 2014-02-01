#include <iostream>
#include <cmath>
#include <array>

using namespace std;

static array<double, 3> to_cart(double lat, double lon)
{
    lat *= M_PI / 180.0;
    lon *= M_PI / 180.0;
    return {{
        cos(lat) * cos(lon), cos(lat) * sin(lon), sin(lat)
    }};
}

static double dist(const array<double, 3> &a, const array<double, 3> &b)
{
    double d = a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
    return acos(d);
}

static double dist(double lat1, double lon1, double lat2, double lon2)
{
    return dist(to_cart(lat1, lon1), to_cart(lat2, lon2));
}

int main()
{
    int N;
    double lat, lon, lat0, lon0;
    double ans = 0;
    cin >> N;
    cin >> lat >> lon;
    lat0 = lat; lon0 = lon;
    for (int i = 1; i < N; i++)
    {
        double lat2, lon2;
        cin >> lat2 >> lon2;
        ans += dist(lat, lon, lat2, lon2);
        lat = lat2;
        lon = lon2;
    }
    ans += dist(lat, lon, lat0, lon0);
    ans *= 6371.0;
    cout << fixed << ans << '\n';
}
