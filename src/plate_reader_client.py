import requests


class PlateReaderClient:
    def __init__(self, host: str):
        self.host = host

    def read_plate_number(self, im):
        res = requests.post(
            f'{self.host}/readPlateNumber',
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            data=im,
        )
        return res.json()


    def greeting(self, user: str):
        res = requests.post(
            f'{self.host}/greeting',
            headers={'Content-Type': 'application/json'},
            json={
                'user': user,
            },
        )
        return res.json()

    def read_plate_number_by_image_id(self, img_id: int):
        res = requests.get(
            f'{self.host}/readPlateNumberById/{img_id}',
        )
        return res.status_code, res.json()

    def read_plate_number_by_multiple_image_ids(self, img_ids: str):
        res = requests.get(
            f'{self.host}/readPlateNumberByMultipleIds/{img_ids}',
        )
        return res.status_code, res.json()


if __name__ == '__main__':
    client = PlateReaderClient(host='http://127.0.0.1:8080')

    res = client.greeting("Kate")
    print(res)

    with open('./images/9965.jpg', 'rb') as im:
        res = client.read_plate_number(im)
        print(res)

    status_code, res = client.read_plate_number_by_image_id(10022)
    print(status_code, res)

    status_code, res = client.read_plate_number_by_image_id(1)
    print(status_code, res)

    status_code, res = client.read_plate_number_by_multiple_image_ids("10022,9965")
    print(status_code, res)

    status_code, res = client.read_plate_number_by_multiple_image_ids("10022,111")
    print(status_code, res)

    status_code, res = client.read_plate_number_by_multiple_image_ids("123;124")
    print(status_code, res)
