# Q3: Single-Neuron Logistic Model for Fruit Classification

This assignment implements a single-neuron logistic regression model to classify fruits (apples vs bananas) using pure NumPy and batch gradient descent.

## Files

- `fruit.csv` - Dataset with fruit characteristics (length_cm, weight_g, yellow_score, label)
- `perceptron.ipynb` - Jupyter notebook with the complete implementation
- `reflection.md` - Analysis and insights about the training process
- `README.md` - This file

## Dataset

The `fruit.csv` file contains 12 samples with the following features:
- `length_cm`: Length of the fruit in centimeters
- `weight_g`: Weight of the fruit in grams  
- `yellow_score`: Yellow color intensity (0-1 scale)
- `label`: Binary classification (0=apple, 1=banana)

## Implementation Details

### Model Architecture
- Single neuron with sigmoid activation function
- 3 input features + 1 bias term
- Binary cross-entropy loss function
- Batch gradient descent optimization

### Training Parameters
- Learning rate: 0.1 (with comparison across multiple rates)
- Maximum epochs: 500
- Convergence threshold: loss < 0.05
- Early stopping when convergence is reached

### Key Features
1. **Pure NumPy Implementation**: No machine learning libraries used for the core algorithm
2. **Batch Gradient Descent**: Updates weights using the entire dataset
3. **Learning Rate Analysis**: Compares convergence across different learning rates
4. **Visualization**: Plots loss and accuracy curves over training epochs
5. **Initial vs Final Comparison**: Shows improvement from random initialization

## Running the Code

1. Ensure you have the required packages:
   ```bash
   pip install numpy pandas matplotlib scikit-learn jupyter
   ```

2. Open the Jupyter notebook:
   ```bash
   jupyter notebook perceptron.ipynb
   ```

3. Run all cells to see the complete training process and analysis.

## Expected Results

- Initial random accuracy: ~50%
- Final trained accuracy: ~100%
- Convergence typically achieved within 100-200 epochs
- Learning rate of 0.1 provides optimal balance of speed and stability

## Learning Outcomes

This assignment demonstrates:
- How gradient descent optimizes model parameters
- The impact of learning rate on convergence
- The relationship between loss and accuracy
- The analogy between machine learning and human learning processes 