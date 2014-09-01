package main
 
import (
    "encoding/csv"
    "fmt"
    "io"
    "os"
)
 
func main() {
    file, err := os.Open("C41295-100_20140220_135315.CSV")
	
    if err != nil {
        fmt.Println("Error:", err)
        return
    }
    
	defer file.Close()
	
    reader := csv.NewReader(file)
	
	reader.Comma = ';'
	
    for {
        record, err := reader.Read()
        if err == io.EOF {
            break
        } else if err != nil {
            fmt.Println("Error:", err)
            return
        }
 
        fmt.Println(record[10], record[11]) // record has the type []string
    }
}
