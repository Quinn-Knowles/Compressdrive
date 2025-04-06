import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def read_compression_data(file_path):
    data = pd.read_csv(file_path, header=None, skiprows=1, 
                       names=["file_name", "original_size", "deflate_size", "deflate_ratio", 
                              "deflate_time", "ppmd_size", "ppmd_ratio", "ppmd_time", 
                              "mx9_size", "mx9_ratio", "mx9_time", "win_size", "win_ratio", "win_time"])
    return data

def plot_compression_ratio_heatmap(data):
    ratio_data = data[["file_name", "deflate_ratio", "ppmd_ratio", "mx9_ratio", "win_ratio"]]
    
    ratio_data.set_index('file_name', inplace=True)
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(ratio_data, annot=True, cmap='coolwarm', cbar=True, linewidths=0.5)
    
    plt.title('Compression Ratios for Different Algorithms')
    plt.tight_layout()
    plt.show()

def plot_compression_time_heatmap(data):
    time_data = data[["file_name", "deflate_time", "ppmd_time", "mx9_time", "win_time"]]
    
    time_data.set_index('file_name', inplace=True)
    plt.figure(figsize=(10, 8))
    sns.heatmap(time_data, annot=True, cmap='YlGnBu', cbar=True, linewidths=0.5)
    
    plt.title('Compression Times for Different Algorithms')
    plt.tight_layout()
    plt.show()

# Main function to load the data and generate heatmaps
def main():
    file_path = "output.txt"  
    compression_data = read_compression_data(file_path)
    
    plot_compression_ratio_heatmap(compression_data)
    plot_compression_time_heatmap(compression_data)

if __name__ == "__main__":
    main()
