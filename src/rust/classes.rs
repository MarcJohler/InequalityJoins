use ndarray::{Array1, Array2};

fn pairs(arr1: &Array1<f64>, arr2: &Array1<f64>) -> Vec<(f64, f64)> {
    let mut output = Vec::new();
    for i in 0..arr1.len() {
        for j in 0..arr2.len() {
            output.push((arr1[i], arr2[j]));
        }
    }
    output
}

use ndarray::arr1;

fn main() {
    let arr1 = arr1(&[1.0, 2.0, 3.0]);
    let arr2 = arr1(&[4.0, 5.0]);
    let output = pairs(&arr1, &arr2);
    println!("Pairs: {:?}", output);
}