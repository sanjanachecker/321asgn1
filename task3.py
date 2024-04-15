import pandas as pd
import matplotlib.pyplot as plt

data = {
    'type': ['16', '64', '256', '1024', '8192', '16384'],
    'aes-128-cbc ': [683631.13, 875013.60,  947499.54, 967702.26, 972842.47, 974727.45],
    'aes-192-cbc': [629472.17, 745077.26, 785131.12, 797110.37, 800854.30, 800273.47],
    'aes-256-cbc': [521489.60, 644780.46, 678785.20, 686413.91, 691728.10, 693103.48],
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