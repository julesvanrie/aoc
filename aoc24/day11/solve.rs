use std::env;
use std::fs;
use std::error::Error;
use std::collections::HashMap;

fn main() -> Result<(), Box<dyn Error>> {
    let input = read_input();
    solve_one(&input);
    solve_two(&input);
    Ok(())
}

fn read_input() -> String {
    let args: Vec<String> = env::args().collect();
    let file_name = format!("{}.txt", &args[1]);
    fs::read_to_string(file_name)
        .unwrap()
}

fn solve_one(input: &str) {
    let stones: Vec<String> = input.split_whitespace().map(|s| s.to_string()).collect();

    let mut tmp = stones;
    for _ in 0..25 {
        let mut new_tmp = vec![];
        for stone in tmp {
            if stone == "0" {
                new_tmp.push("1".to_string())
            } else {
                if stone.len() % 2 == 0 {
                    if stone.len() > 1 {
                        new_tmp.push(stone[..(stone.len()/2)].to_string());
                        new_tmp.push(stone[(stone.len()/2)..].parse::<i64>().unwrap().to_string());
                    } else {
                        new_tmp.push((stone.parse::<i64>().unwrap() * 2024).to_string());
                    }
                } else {
                    new_tmp.push((stone.parse::<i64>().unwrap() * 2024).to_string());
                }
            }
        }
        tmp = new_tmp;
    }

    let result = tmp.len();

    println!("The answer for part 1 is: {}", result);
}

fn solve_two(input: &str) {
    let stones: Vec<String> = input.split_whitespace().map(|s| s.to_string()).collect();

    let mut cache: HashMap<(String, i8), i64> = HashMap::new();

    let result: i64 = stones.into_iter()
                             .map(|s| get_count_with_cache(s, 75, &mut cache))
                             .sum();

    println!("The answer for part 2 is: {}", result);
}

fn get_count_with_cache(
    stone: String,
    i: i8,
    cache: &mut HashMap<(String, i8), i64>
) -> i64 {
    // First check the cache
    if let Some(res) = cache.get(&(stone.clone(), i)) {
        return *res;
    } else {
        let res = get_count(stone.clone(), i, cache);
        // Update the cache
        cache.insert((stone, i), res);
        return res
    }
}

fn get_count(
    stone: String,
    i: i8,
    cache: &mut HashMap<(String, i8), i64>
) -> i64 {
    // Finished iterations so return 1
    if i == 0 {
        return 1
    }
    // Not finished iterations
    // 0 becomes 1
    if stone == "0" {
        return get_count_with_cache("1".to_string(), i-1, cache)
    }
    // If even, split
    if stone.len() % 2 == 0 {
        let mid = stone.len() / 2;
        let left = stone[..mid].to_string();
        let right = (stone[mid..].parse::<i64>().unwrap()).to_string();
        return get_count_with_cache(left, i-1, cache)
             + get_count_with_cache(right, i-1, cache)
    }
    // Not even, so multiply by 2024
    let next = (stone.parse::<i64>().unwrap() * 2024).to_string();
    return get_count_with_cache(next, i-1, cache)
}
