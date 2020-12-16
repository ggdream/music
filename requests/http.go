package requests

import (
	"net/http"
	"time"
)

func genRequest(method string, url string, headers map[string]interface{}) *http.Request {
	req, err := http.NewRequest(method, url, nil)
	if err != nil {
		panic(err.Error())
	}

	for k, v := range headers {
		req.Header.Add(k, v.(string))
	}
	return req
}

func Get(url string, headers map[string]interface{}) *http.Response {
	client := &http.Client{Timeout: 3 * time.Second}
	req := genRequest(http.MethodGet, url, headers)

	res, err := client.Do(req)
	if err != nil {
		panic(err.Error())
	}
	return res
}
