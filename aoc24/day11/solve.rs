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
    let stones: Vec<i64> = input.split_whitespace()
                                 .map(|s| s.parse().unwrap())
                                 .collect();

    let mut tmp = stones;
    for _ in 0..25 {
        let mut new_tmp = vec![];
        for stone in tmp {
            if stone == 0 {
                new_tmp.push(1)
            } else {
                let s = stone.to_string();
                if s.len() % 2 == 0 {
                    if s.len() > 1 {
                        new_tmp.push(s[..(s.len()/2)].parse().unwrap());
                        new_tmp.push(s[(s.len()/2)..].parse().unwrap());
                    } else {
                        new_tmp.push(stone * 2024);
                    }
                } else {
                    new_tmp.push(stone * 2024);
                }
            }
        }
        tmp = new_tmp;
    }

    let result = tmp.len();

    println!("The answer for part 1 is: {}", result);
}

fn solve_two(input: &str) {
    let stones: Vec<i64> = input.split_whitespace()
                                 .map(|s| s.parse().unwrap())
                                 .collect();

    let mut cache: HashMap<(i64, i8), i64> = HashMap::new();

    let result: i64 = stones.into_iter()
                             .map(|s| get_count_with_cache(s, 75, &mut cache))
                             .sum();

    println!("The answer for part 2 is: {}", result);
}

fn get_count_with_cache(
    stone: i64,
    i: i8,
    cache: &mut HashMap<(i64, i8), i64>
) -> i64 {
    // First check the cache
    if let Some(res) = cache.get(&(stone, i)) {
        return *res;
    } else {
        let res = get_count(stone, i, cache);
        // Update the cache
        cache.insert((stone, i), res);
        return res
    }
}

fn get_count(
    stone: i64,
    i: i8,
    cache: &mut HashMap<(i64, i8), i64>
) -> i64 {
    // Finished iterations so return 1
    if i == 0 {
        return 1
    }
    // Not finished iterations
    // 0 becomes 1
    if stone == 0 {
        return get_count_with_cache(1, i-1, cache)
    }
    // If even, split
    let s = stone.to_string();
    if s.len() % 2 == 0 {
        let mid = s.len() / 2;
        let left = s[..mid].parse().unwrap();
        let right = s[mid..].parse().unwrap();
        return get_count_with_cache(left, i-1, cache)
             + get_count_with_cache(right, i-1, cache)
    }
    // Not even, so multiply by 2024
    return get_count_with_cache(stone * 2024, i-1, cache)
}
