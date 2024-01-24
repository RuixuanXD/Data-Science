import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import signal, fft
import seaborn
import os
import fnmatch
seaborn.set()


def plot_atotal(data, filename):
    """
    Plot the original atotal data and filtered atotal data respectively over time
    :param data: processed data
    :param filename: name of each csv file
    :return: none
    """
    plt.figure()
    plt.plot(data['time'], data['atotal'])
    plt.title('Original Total Acceleration')
    plt.xlabel('Time')
    plt.ylabel('Total Acceleration')
    plt.savefig('figures_data/' + str(filename) + '_origin' + '.jpg')
    plt.close()

    plt.figure()
    plt.plot(data['time'], data['lowpass'])
    plt.title('Filtered Total Acceleration with Lowpass')
    plt.xlabel('Time')
    plt.ylabel('Total Acceleration')
    plt.savefig('figures_data/' + str(filename) + '_lowpass' + '.jpg')
    plt.close()

    plt.figure()
    plt.plot(data['frequency'], data['ft_atotal'])
    plt.title('Transformed Total Acceleration with Fourier Transform')
    plt.xlabel('Frequency')
    plt.savefig('figures_data/' + str(filename) + '_ft' + '.jpg')
    plt.close()


def data_processing(filenames, path):
    """
    Clean and process the raw data with Lowpass filter and Fourier Transform, and add the frequency to data file
    :param path: path of folder
    :param filenames: a list of all filenames in the dataset folder
    :return: freq_data: a list of frequency generated from each .csv file in filenames
    """
    freq_data = []
    for filename in filenames:
        data = pd.read_csv(path + str(filename) + '.csv')
        # ignore the first 3s and the last 3s
        data = data[data['time'] > 3]
        data = data[data['time'] < (data['time'].iloc[-1] - 3)]

        atotal = data['atotal']  # atotal is total acceleration collected by the app PhysicsToolbox Suite
        b, a = signal.butter(N=3, Wn=0.1, btype='lowpass', analog=False)  # apply Nth-order digital Butterworth filter
        lowpass_atotal = signal.filtfilt(b, a, atotal)  # apply a digital filter forward and backward to a signal
        data['lowpass'] = lowpass_atotal

        # Apply Fast Fourier Transform to lowpass_atotal (changes the domain (x-axis) of a signal from time to frequency)
        data['ft_atotal'] = fft.fft(lowpass_atotal)
        data['ft_atotal'] = fft.fftshift(data['ft_atotal'])  # shift the zero-freq component to the center of the spectrum
        data['ft_atotal'] = abs(data['ft_atotal'])

        # Calculate frequency (frequency = number of data / time difference between first data and last data)
        first_data = data['time'].iloc[0]
        last_data = data['time'].iloc[-1]
        frequency = round(len(data) / (last_data - first_data))
        data['frequency'] = np.linspace(-frequency/2, frequency/2, num=len(data))

        # Plot the original atotal, lowpass atotal and FT atotal over time
        plot_atotal(data, filename)

        # Get the frequency at the largest ft value for frequency > 0.1
        data = data[data['frequency'] > 0.1]
        idx = data['ft_atotal'].idxmax()           # index of the largest ft_atotal value
        sample_freq = data.at[idx, 'frequency']    # frequency value at the largest ft_atotal value
        freq_data.append(sample_freq)
        # print(freq_data)

    return freq_data


def save_to_file(data_path, freq_data):
    """
    Save the data of frequency to summary.csv file
    :param data_path: path of the summary.csv file
    :param freq_data: a list of frequency generated from each .csv file in dataset folder
    :return: none
    """
    data = pd.read_csv(data_path)
    data['frequency'] = freq_data
    data.to_csv(data_path, index=False)
    # print(summary)


def main():
    # process general data
    path = r'dataset/'
    file_count = len(fnmatch.filter(os.listdir(path), '*.csv')) - 1  # number of .csv files in the dataset folder
    filenames = np.arange(1, file_count + 1)          # list of filenames (all files are named by numbers)
    freq_data = data_processing(filenames, path)            # processing each file
    save_to_file(path + 'summary.csv', freq_data)            # save the frequency data to the summary file

    # process specific data for flat ground, upstairs, and downstairs
    path_flat = r'dataset/flat/'
    path_up = r'dataset/upstairs/'
    path_down = r'dataset/downstairs/'
    file_count_flat = len(fnmatch.filter(os.listdir(path_flat), '*.csv')) - 1
    file_count_up = len(fnmatch.filter(os.listdir(path_up), '*.csv')) - 1
    file_count_down = len(fnmatch.filter(os.listdir(path_down), '*.csv')) - 1
    filenames_flat = np.arange(100, file_count_flat + 100)
    filenames_up = np.arange(200, file_count_up + 200)
    filenames_down = np.arange(300, file_count_down + 300)
    freq_flat = data_processing(filenames_flat, path_flat)
    freq_up = data_processing(filenames_up, path_up)
    freq_down = data_processing(filenames_down, path_down)
    save_to_file(path_flat + 'flat.csv', freq_flat)
    save_to_file(path_up + 'upstairs.csv', freq_up)
    save_to_file(path_down + 'downstairs.csv', freq_down)
    print('Data cleaning and processing is finished.')


if __name__ == '__main__':
    main()
