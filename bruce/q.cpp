#include <iostream>
#include <vector>
#include <algorithm>
#include <cassert>
#include <fftw3.h>
#include <sox.h>

using namespace std;

/**
 * Read an entire sound file into memory, as 32-bit sign integer values.
 * The file format is auto-detected from the filename.
 *
 * @param      fname      Input filename
 * @param[out] rate       Sampling rate
 * @param[out] channels   Number of input channels (interleaved)
 * @param[out] precision  Number of bits per channel in file
 *
 * @return Vector of 32-bit signed integer samples
 */
std::vector<int32_t> sound_read_from_file(
    const char *fname,
    double &rate,
    unsigned int &channels,
    unsigned int &precision)
{
    sox_format_init();

    sox_format_t *handle = sox_open_read(fname, NULL, NULL, NULL);
    if (handle == NULL)
    {
        cerr << "Could not open " << fname << '\n';
        exit(1);
    }

    std::vector<int32_t> ans;
    sox_sample_t buffer[4096];
    size_t sz;
    while ((sz = sox_read(handle, buffer, sizeof(buffer) / sizeof(buffer[0]))) > 0)
    {
        std::copy(buffer, buffer + sz, std::back_inserter(ans));
    }

    rate = handle->signal.rate;
    channels = handle->signal.channels;
    precision = handle->signal.precision;
    sox_close(handle);

    sox_format_quit();
    return ans;
}

int main(int argc, char **argv)
{
    assert(argc == 2);
    const int irate = 44100;
    double rate;
    unsigned int channels, precision;
    vector<int32_t> signal = sound_read_from_file(argv[1], rate, channels, precision);
    assert(rate == irate);
    assert(channels == 1);
    assert(precision == 8);

    double *window = fftw_alloc_real(irate);
    fftw_complex *out = fftw_alloc_complex(irate / 2 + 1);
    fftw_plan plan = fftw_plan_dft_r2c_1d(irate, window, out, FFTW_ESTIMATE);
    int best = 0;
    int bestT = 0;
    for (size_t i = 0; i + irate <= signal.size(); i += irate)
    {
        for (int j = 0; j < irate; j++)
            window[j] = signal[i + j];
        fftw_execute(plan);
        int score = 0;
        for (int f = 500; f <= 10000; f += 100)
        {
            double e = out[f][0] * out[f][0] + out[f][1] * out[f][1];
            if (e > 3e23)
            {
                cerr << i / irate << ", " << f << ": " << e * 1e-23 << '\n';
                score++;
            }
        }
        if (score > best)
        {
            best = score;
            bestT = i / irate;
        }
    }
    cout << best << ' ' << bestT + 1 << '\n';
}
