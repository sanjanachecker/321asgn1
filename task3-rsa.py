import pandas as pd
import matplotlib.pyplot as plt

key_sizes = [512, 1024, 2048, 3072, 4096, 7680, 15360]
sign_throughput = [33189.7, 6908.0,
                   1113.6, 382.9, 174.9, 21.1, 4.0]

# RSA
plt.figure(figsize=(10, 6))


# Scatter plot for signing throughput
plt.scatter(key_sizes, sign_throughput, label='Sign', marker='o', color='blue')


# plt.xscale('log')  # Use a logarithmic scale for better visibility
# plt.yscale('log')
plt.xlabel('RSA key size (bits)')
plt.ylabel('signing throughput (operations per second)')
plt.title('Signing throughput vs RSA key size')
plt.legend()
plt.grid(True)
plt.show()
