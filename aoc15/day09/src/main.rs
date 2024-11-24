use std::env;
use std::fs;
use std::error::Error;
use std::collections::HashMap;
use std::collections::HashSet;
extern crate regex;
use regex::Regex;

fn main() -> Result<(), Box<dyn Error>> {
    let input = read_input();

    solve(&input)?;

    Ok(())
}

fn read_input() -> String {
    let args: Vec<String> = env::args().collect();
    let file_name = format!("{}.txt", &args[1]);
    fs::read_to_string(file_name)
        .unwrap()
}

fn solve(input: &String) -> Result<(), Box<dyn Error>> {
    let mut min_distance = i32::max_value();
    let mut max_distance = 0i32;

    let mut cities = HashSet::<String>::new();
    let mut distances = HashMap::<String, i32>::new();

    let re = Regex::new(
        r###"(?m)^([A-z]+) to ([A-z]+) = (\d+)$"###
    ).unwrap();

    for (_, [start, end, distance])
         in re.captures_iter(input).map(|c| c.extract()) {
        cities.insert(start.to_string());
        cities.insert(end.to_string());
        distances.insert(
            format!("{} {}", start, end),
            distance.parse().unwrap()
        );
        distances.insert(
            format!("{} {}", end, start),
            distance.parse().unwrap()
        );
    }

    let permutations = heaps_algo(cities.len(), &mut cities.iter().collect());

    for permutation in permutations {
        let mut distance = 0;
        for i in 0..cities.len()-1 {
            distance += distances.get(
                &*format!("{} {}", permutation[i], permutation[i+1])
            ).unwrap()
        }
        min_distance = std::cmp::min(distance, min_distance);
        max_distance = std::cmp::max(distance, max_distance);

    }

    println!("The answer for part 1 is: {}", min_distance);
    println!("The answer for part 2 is: {}", max_distance);
    Ok(())
}

fn heaps_algo<T: Clone>(k: usize, arr: &mut Vec<T>) -> Vec<Vec<T>>{
    match k {
        1 => vec![arr.to_vec()],
        _ => {
            let mut permutations = heaps_algo(k-1, arr);
            for i in 0..k-1 {
                match k % 2 {
                    0 => arr.swap(i, k-1),
                    _ => arr.swap(0, k-1)
                }
                permutations.extend(heaps_algo(k-1, arr));
            }
            permutations
        }
    }
}
