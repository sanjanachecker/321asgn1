import pandas as pd
import matplotlib.pyplot as plt

data = {
    'type': ['16', '64', '256', '1024', '8192', '16384'],
    'aes-128-cbc': [683631.13, 875013.60,  947499.54, 967702.26, 972842.47, 974727.45],
    'aes-192-cbc': [629472.17, 745077.26, 785131.12, 797110.37, 800854.30, 800273.47],
    'aes-256-cbc': [521489.60, 644780.46, 678785.20, 686413.91, 691728.10, 693103.48],
    'aes-128-ecb': [742447.17, 2768546.47, 5891711.32, 8428683.26, 9387911.45, 9491623.81],
    'aes-192-ecb': [708206.36, 2543329.52, 5269600.32, 7248576.81, 7929492.82, 8031113.50],
    'aes-256-ecb': [619678.97, 2254062.48, 4707154.49, 6237943.82, 6696706.84, 6748062.88]
}

df = pd.DataFrame(data)

# Plotting
plt.figure(figsize=(12, 6))
for col in df.columns[1:]:
    plt.plot(df['type'], df[col], marker='o', label=col)

plt.title('AES Throughput')
plt.xlabel('AES Type')
plt.ylabel('Throughput (k)')
plt.xticks(rotation=45)
plt.legend(title='Data Size')
plt.grid(True)
plt.tight_layout()
plt.show()