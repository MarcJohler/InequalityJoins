use ndarray::array;

mod classes;

fn main() {
    let arr1 = array![1, 2, 3];
    let arr2 = array![4, 5];
    let pairs = classes::pairs((&arr1).into(), (&arr2).into());
    println!("{:?}", pairs);
}