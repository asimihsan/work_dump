library(ggplot2)

andromeda <- c(7.67, 7.47, 7.22, 7.66, 9.9, 8.23, 8.22, 7.4, 9.01, 8.64, 8.65, 7.27, 7.24, 11.5, 7.39, 7.2, 7.19, 8.18, 10.4, 7.79, 8.76, 7.38, 7.58, 10.8, 7.54, 7.45, 7.14, 10.7, 9.3, 7.23, 7.35, 7.37, 10.6, 7.29, 7.38, 8.77, 8.36, 9.25, 7.16, 7.51, 7.7, 9.81, 8.92, 7.59, 7.32, 7.61, 10, 9.19, 7.14, 8.43, 9.47, 7.45, 7.39, 8.64, 11.3, 8.35, 7.63, 7.41, 9.56, 8.48, 7.25, 7.92, 21, 7.95, 7.24, 7.52, 9.8, 8.61, 8.36, 7.22, 7.61, 10.4, 7.54, 7.3, 8, 9.8, 8.37, 7.71, 7.77, 7.77, 11, 7.86, 8.26, 7.63, 8.58, 9.41, 7.26, 8.16, 7.18, 10.7, 8.78, 7.89, 8.45, 9.7, 8.28, 7.47, 7.71, 11.9, 9.37, 7.34)
gemini <- c(7.2, 6.81, 7.26, 9.29, 7.65, 6.89, 7.78, 9.06, 9.13, 7.49, 7.09, 6.93, 7.83, 9.54, 7.26, 7.77, 7.03, 9.86, 6.92, 7.03, 7.44, 7.69, 10.9, 7.65, 7.32, 7.11, 7.23, 9.62, 8.48, 6.89, 7.39, 8.22, 8.53, 7.51, 7.12, 6.9, 9.98, 7.83, 7.39, 6.91, 6.87, 9.7, 7.34, 7.27, 7.88, 9.1, 9.49, 7.14, 7.1, 7.39, 7.25, 6.87, 7.43, 8.06, 9.13, 8.44, 17.1, 9.97, 7.29, 7.52, 7.66, 10.6, 9.31, 7.19, 7.31, 7.03, 10.4, 8.02, 7.79, 7.46, 7.79, 8.99, 7.84, 6.89, 6.99, 8.15, 10.1, 7.24, 6.82, 7.37, 8.82, 8.88, 7.06, 6.95, 8.11, 9.14, 7.54, 7.29, 7.42, 7.08, 9.4, 8.8, 7.39, 6.93, 7.72, 9.38, 9, 7, 6.9, 11.1)
scorpius <- c(9.24, 7.31, 8.34, 7.53, 9.45, 6.91, 7.13, 8.52, 9.11, 6.86, 7.06, 12, 9.37, 7.08, 6.84, 7.05, 8.98, 7.47, 6.87, 6.96, 8.83, 7.85, 7.68, 6.92, 7.18, 8.86, 7.16, 8.22, 7.2, 8.23, 7, 7.23, 7.82, 7.27, 8.68, 9.08, 7.6, 7.04, 8.57, 7.34, 8.1, 7.18, 8.5, 8.15, 7.22, 6.98, 9.74, 7.22, 7.39, 7.6, 8.29, 7, 7.98, 6.9, 8.71, 7.11, 8.9, 7.37, 7.23, 7.48, 8.96, 8.41, 8.53, 7.53, 7.22, 9.51, 7.52, 7.09, 7.17, 9.97, 7.33, 6.83, 7.83, 8.48, 7.04, 7.94, 6.94, 8.58, 7.85, 7.68, 7.32, 7.24, 8.21, 7.17, 7.51, 7.71, 8.55, 6.88, 8.24, 7.1, 7.35, 7.74, 6.85, 8.25, 7.51, 9.2, 7.54, 7.25, 7.6, 10.3)
draco <- c(14.7, 29.6, 10.7, 7.82, 9.05, 25.6, 16.5, 8.53, 9.95, 27, 15.9, 8.55, 9.84, 24.9, 20.1, 9.65, 27.7, 12.7, 10.2, 16.6, 30.6, 9.28, 12.8, 11.3, 26.6, 14.3, 10.7, 29.5, 13.4, 10.3, 13.5, 25.1, 9.22, 10.1, 11.9, 30.4, 8.36, 9.52, 37.8, 8.23, 8.24, 10.5, 30.3, 8.8, 13.8, 10, 9.35, 30.3, 8.39, 10.1, 8.63, 30.3, 8.89, 8.01, 10.8, 31.9, 8.58, 8.36, 8.37, 18.2, 10.2, 12.7, 11.7, 14.5, 34.5, 8.85, 7.85, 11.1, 31.9, 8.87, 8, 13.9, 33.2, 9.16, 7.81, 8.82, 32.4, 9.1, 8.66, 8.44, 31.9, 8.96, 15.3, 25, 15.7, 8.34, 8.68, 8.1, 29, 11.1, 8.23, 8.63, 28.4, 9.52, 11.5, 10.8, 27.4, 9.18, 8.17, 15.4)
leo <- c(12.3, 7.77, 10.1, 32.2, 13.9, 9.55, 26.7, 11, 8.19, 8.24, 11.1, 35.5, 9.1, 7.8, 8.02, 37.1, 15.7, 60, 60, 60, 28.6, 17.4, 12.7, 9.49, 33.6, 9.63, 8.73, 7.77, 42.8, 8.36, 27.8, 11.9, 11.8, 10.3, 35, 12, 8.02, 8.07, 25.5, 18.5, 8.69, 8.97, 29.1, 9.46, 60, 60, 18.1, 28.7, 9.22, 8.47, 11.6, 8.07, 29.2, 19, 24.1, 60, 60, 60, 49.2, 8.69, 24.6, 11.5, 11.1, 11.5, 26.4, 12.8, 9.03, 38.5, 11.4, 14.3, 10.6, 33.6, 8.57, 7.87, 7.98, 25.6, 19.4, 9.17, 8.07, 27.2, 7.93, 11.5, 40.3, 10, 8.81, 10.4, 40.1, 13.3, 10.9, 26.7, 12, 10.4, 9.15, 38.2, 11.6, 10.7, 26.4, 10.8, 8.41, 8.88)
libra <- c(9.82, 7.43, 8.93, 8.09, 7.14, 7.75, 7.16, 9.44, 10.1, 6.55, 8.12, 8.78, 7.66, 6.71, 7.86, 9.9, 10.6, 6.81, 7.23, 9.59, 7.23, 7.15, 8.18, 8.26, 11.1, 7.07, 7.43, 8.65, 9.5, 7.11, 9.6, 8.2, 11.2, 7.02, 8.24, 7.73, 12.5, 8.03, 7.44, 7.73, 11.2, 7.41, 8.28, 7.29, 8.77, 8.35, 10.3, 8.66, 13.1, 8.18, 7.64, 8.44, 9.57, 9.03, 9.38, 9.7, 7.19, 8.02, 7.71, 10.2, 8.2, 7.72, 9.4, 13.6, 8.11, 7.12, 7.23, 9.55, 7.28, 8.46, 9.85, 8.52, 8.47, 7.41, 7.19, 8.86, 7.36, 8.41, 9.94, 7, 9.26, 7.29, 7.09, 6.98, 9.48, 8.01, 10.7, 6.91, 9.42, 7.82, 7.06, 7.08, 10.5, 8.15, 11.7, 7.26, 9.87, 6.99, 7.68, 7.02)

andromeda_d = density(x=andromeda, bw=0.25)
draco_d = density(draco, bw=0.25)
gemini_d = density(gemini, bw=0.25)
leo_d = density(leo, bw=0.25)
scorpius_d = density(scorpius, bw=0.25)
libra_d = density(libra, bw=0.25)

x_min <- 0
x_max <- 60

par(mfrow=c(3,1))
plot(andromeda_d, xlim=c(x_min, x_max))
lines(gemini_d, xlim=c(x_min, x_max))
lines(scorpius_d, xlim=c(x_min, x_max))
grid()
plot(draco_d, xlim=c(x_min, x_max))
lines(leo_d, xlim=c(x_min, x_max))
grid()
plot(libra_d, xlim=c(x_min, x_max))
grid()

#andromeda_c = ecdf(x=andromeda)
#draco_c = ecdf(x=draco)
#gemini_c = ecdf(x=gemini)
#leo_c = ecdf(x=leo)
#draco_c = ecdf(x=draco)
#scorpius_c = ecdf(x=scorpius)
#libra_c = ecdf(x=libra)

#par(mfrow=c(3,1))
#plot(andromeda_c, xlim=c(x_min, x_max))
#lines(gemini_c, xlim=c(x_min, x_max))
#lines(scorpius_c, xlim=c(x_min, x_max))
#grid()
#plot(draco_c, xlim=c(x_min, x_max))
#lines(leo_c, xlim=c(x_min, x_max))
#grid()
#plot(libra_c, xlim=c(x_min, x_max))
