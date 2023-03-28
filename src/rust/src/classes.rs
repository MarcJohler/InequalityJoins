use ndarray::ArrayView1;

pub fn pairs(arr1: ArrayView1<i32>, arr2: ArrayView1<i32>) -> Vec<(i32, i32)> {
    let mut output = vec![];
    for i in 0..arr1.len() {
        for j in 0..arr2.len() {
            output.push((arr1[i], arr2[j]));
        }
    }
    output
}