
/*
https://github.com/MisterF21/csv2json/blob/master/csv2json.go
*/

package csv2json

import (
    "encoding/csv"
    "encoding/json"
    "io"
)

func Convert(r io.Reader, columns []string) ([]byte, error) {
    rows := make([]map[string]string, 0)
    csvReader := csv.NewReader(r)
    csvReader.TrimLeadingSpace = true
    for {
        record, err := csvReader.Read()
        if err == io.EOF {
            break
        }
        if err != nil {
            return nil, err
        }
        row := make(map[string]string)
        for i, n := range columns {
            row[n] = record[i]
        }
        rows = append(rows, row)
    }
    data, err := json.MarshalIndent(&rows, "", "  ")
    if err != nil {
        return nil, err
    }
    return data, nil
}