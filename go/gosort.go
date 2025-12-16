// ENES YILDIRIM 211ADB121
package main

import (
	"bufio"
	"errors"
	"flag"
	"fmt"
	"log"
	"math"
	"math/rand"
	"os"
	"sort"
	"strconv"
	"strings"
	"sync"
	"time"
)

// -----------------------------
// Entry point
// -----------------------------

func main() {
	r := flag.Int("r", -1, "generate N random integers (N >= 10)")
	i := flag.String("i", "", "input file")
	flag.Parse()

	switch {
	case *r != -1:
		if err := runRandom(*r); err != nil {
			log.Fatal(err)
		}
	case *i != "":
		if err := runInputFile(*i); err != nil {
			log.Fatal(err)
		}
	default:
		log.Fatal("Usage: gosort -r N | -i input.txt")
	}
}

// -----------------------------
// -r mode
// -----------------------------

func runRandom(n int) error {
	if n < 10 {
		return errors.New("N must be >= 10")
	}

	numbers := generateRandomNumbers(n)
	runAndPrint(numbers)
	return nil
}

// -----------------------------
// -i mode
// -----------------------------

func runInputFile(filename string) error {
	numbers, err := readNumbersFromFile(filename)
	if err != nil {
		return err
	}

	if len(numbers) < 10 {
		return errors.New("input file must contain at least 10 integers")
	}

	runAndPrint(numbers)
	return nil
}

// -----------------------------
// Shared pipeline
// -----------------------------

func runAndPrint(numbers []int) {
	fmt.Println("Original numbers:")
	fmt.Println(numbers)

	chunks := splitIntoChunks(numbers)

	fmt.Println("\nChunks before sorting:")
	printChunks(chunks)

	sortedChunks := sortChunksConcurrently(chunks)

	fmt.Println("\nChunks after sorting:")
	printChunks(sortedChunks)

	result := mergeSortedChunks(sortedChunks)

	fmt.Println("\nFinal sorted result:")
	fmt.Println(result)
}

// -----------------------------
// Chunking
// -----------------------------

func splitIntoChunks(numbers []int) [][]int {
	n := len(numbers)

	numChunks := int(math.Ceil(math.Sqrt(float64(n))))
	if numChunks < 4 {
		numChunks = 4
	}

	base := n / numChunks
	extra := n % numChunks

	var chunks [][]int
	start := 0

	for i := 0; i < numChunks && start < n; i++ {
		size := base
		if i < extra {
			size++
		}

		end := start + size
		if end > n {
			end = n
		}

		chunks = append(chunks, numbers[start:end])
		start = end
	}

	return chunks
}

// -----------------------------
// Concurrent sorting
// -----------------------------

func sortChunksConcurrently(chunks [][]int) [][]int {
	var wg sync.WaitGroup

	for i := range chunks {
		wg.Add(1)
		go func(idx int) {
			defer wg.Done()
			sort.Ints(chunks[idx])
		}(i)
	}

	wg.Wait()
	return chunks
}

// -----------------------------
// Merge logic
// -----------------------------

func mergeSortedChunks(chunks [][]int) []int {
	total := 0
	for _, c := range chunks {
		total += len(c)
	}

	result := make([]int, 0, total)
	indexes := make([]int, len(chunks))

	for len(result) < total {
		minChunk := -1
		var minVal int

		for i, c := range chunks {
			if indexes[i] < len(c) {
				v := c[indexes[i]]
				if minChunk == -1 || v < minVal {
					minVal = v
					minChunk = i
				}
			}
		}

		result = append(result, minVal)
		indexes[minChunk]++
	}

	return result
}

// -----------------------------
// Helpers
// -----------------------------

func generateRandomNumbers(n int) []int {
	rand.Seed(time.Now().UnixNano())
	nums := make([]int, n)
	for i := range nums {
		nums[i] = rand.Intn(1000) // 0–999
	}
	return nums
}

func readNumbersFromFile(filename string) ([]int, error) {
	file, err := os.Open(filename)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	var nums []int
	scanner := bufio.NewScanner(file)

	for scanner.Scan() {
		line := strings.TrimSpace(scanner.Text())
		if line == "" {
			continue
		}

		val, err := strconv.Atoi(line)
		if err != nil {
			return nil, errors.New("invalid integer in file")
		}
		nums = append(nums, val)
	}

	return nums, nil
}

func printChunks(chunks [][]int) {
	for i, c := range chunks {
		fmt.Printf("Chunk %d: %v\n", i, c)
	}
}
