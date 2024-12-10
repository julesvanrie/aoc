use std::env;
use std::fs;
use std::error::Error;
use std::str::FromStr;
use std::collections::HashMap;



fn main() -> Result<(), Box<dyn Error>> {
    let input = read_input();
    solve(input);
    Ok(())
}

fn read_input() -> String {
    let args: Vec<String> = env::args().collect();
    let file_name = format!("{}.txt", &args[1]);
    fs::read_to_string(file_name)
        .unwrap()
}

fn solve(input: String) {

    let (rules_str, updates_str): (String, String) = input.split_once("\n\n").into_iter().collect();

    let rules: Vec<(i32,i32)> =
        rules_str.lines()
                 .map(|line|
                    line.split_once('|')
                         .map(|t|
                              (t.0.parse().unwrap(),
                               t.1.parse().unwrap()))
                         .unwrap())
                 .collect();

    let updates: Vec<Vec<i32>> =
        updates_str.lines()
                   .map(|line|
                         line.split(',')
                             .map(|x| i32::from_str(x).unwrap())
                             .collect())
                   .collect();

    let correct_updates = updates.clone().into_iter()
                                 .filter(|upd| is_valid(upd, &rules))
                                 .collect();

    let result_one = calc_middles(correct_updates);
    println!("The answer for part 1 is: {}", result_one);

    let incorrect_updates = updates.clone().into_iter()
                                   .filter(|upd| !is_valid(upd, &rules))
                                   .map(|upd| correct_update(&upd, &rules))
                                   .collect();

    let result_two = calc_middles(incorrect_updates);
    println!("The answer for part 2 is: {}", result_two);
}

fn is_valid(update: &Vec<i32>, rules: &Vec<(i32, i32)>) -> bool {
    let page_pos = get_page_pos(update);
    for (left, right) in rules {
        if let Some(l_pos) = page_pos.get(&left) {
            if let Some(r_pos) = page_pos.get(&right) {
                if l_pos > r_pos {
                    return false;
                }
            }
        }
    }
    return true;
}

fn calc_middles(updates: Vec<Vec<i32>>) -> i32 {
    updates.into_iter().map(|update| {
        let middle_pos = (update.len()-1) / 2;
        update[middle_pos]
    }).sum()
}

fn correct_update(update: &Vec<i32>, rules: &Vec<(i32, i32)>) -> Vec<i32> {
    if is_valid(update, &rules) {
        return update.to_vec()
    }
    let mut page_pos = get_page_pos(update);
    let mut new_page_pos = page_pos.clone();
    for (left, right) in rules {
        if let Some(l_pos) = page_pos.get(&left) {
            if let Some(r_pos) = page_pos.get(&right) {
                if l_pos > r_pos {
                    new_page_pos.insert(*left, *r_pos);
                    new_page_pos.insert(*right, *l_pos);
                    let mut new_order = new_page_pos.iter().collect::<Vec<(&i32, &usize)>>();
                    new_order.sort_by(|a, b| a.1.cmp(b.1));
                    return correct_update(&new_order.into_iter().map(|(k, v)| *k)
                                       .collect(), &rules);

                }
            }
        }
    }
    return update.to_vec()
}

fn get_page_pos(update: &Vec<i32>) -> HashMap<i32, usize> {
    update.into_iter()
            .enumerate()
            .map(|p| (*p.1, p.0))
            .collect()
}
