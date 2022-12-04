#include <stdio.h>
#include <string.h>
#include <time.h>

void solve(int argc, char *argv[])
{
  char filename[20] = "";
  strcat(filename, argc > 1 ? argv[1] : "input");
  strcat(filename, ".txt");
  FILE *textfile;
  int MAX_LENGTH = 20;
  char line[MAX_LENGTH];
  long result1 = 0; long result2 = 0;

  textfile = fopen(filename, "r");
  while (fgets(line, MAX_LENGTH, textfile))
  {
    int first_left; int first_right; int second_left; int second_right;
    sscanf(line, "%i-%i,%i-%i\n",
      &first_left, &first_right, &second_left, &second_right);
    if (first_left <= second_left && first_right >= second_right
      || first_left >= second_left && first_right <= second_right)
      result1++;
    if (!(first_right < second_left || first_left > second_right))
      result2++;
  }

  fclose(textfile);

  printf("The result for part 1 is %li\n", result1);
  printf("The result for part 2 is %li\n", result2);
}

float timed_solve(int argc, char *argv[]) {
  clock_t start, end;
  double cpu_time_used;
  freopen("/dev/null", "w", stdout);
  start = clock();
  int number = 20;
  for (int i = 0; i < number; i++) {
    solve(1, argv);
  }
  end = clock();
  freopen("/dev/tty", "w", stdout);
  return ((double)(end - start)) / CLOCKS_PER_SEC / number;
}

int main(int argc, char **argv)
{
  if (argc > 1 && !strncmp(argv[1], "time", 4)) {
    printf("This took %f seconds\n", timed_solve(1, argv));
  } else {
    solve(argc, argv);
  }
}
