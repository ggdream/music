package cloud163

import (
	"fmt"
	"github.com/ggdream/music/requests"
	"io"
	"os"
)

func GetById(id string) error {
	res := requests.Get(fmt.Sprintf("http://music.163.com/song/media/outer/url?id=%s.mp3", id), map[string]interface{}{
		"user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36",
	})
	defer res.Body.Close()
	file, err := os.Create(fmt.Sprintf("%s.mp3", id))
	if err != nil {
		return err
	}
	defer file.Close()
	_, err = io.Copy(file, res.Body)
	return err
}
