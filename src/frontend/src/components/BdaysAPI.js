export class BdaysAPI {

  constructor(baseUrl) {
    this.baseUrl = baseUrl;
  }

  listAll() {
    // todo: add pagination
    const bdays = [];
    fetch(this.baseUrl + 'bdays/list')
      .then(response => {
        if (response.ok) {
          return response.json();
        }
      })
      .then(data => {
        for (const i in data) {
          bdays.push(data[i]);
        }
      });
    return bdays;
  }

  add(bdayData) {
    var newBday = null;
    fetch(this.baseUrl + "bday", {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(bdayData)
    })
      .then(response => {
        if (!response.ok) {
          console.log('Could not add birthday' + response);
        } else {
          return response.json();
        }
      })
      .then(data => {
        newBday = data;
      });
    return newBday;
  }

  delete(bdayId) {
    fetch(this.baseUrl + bdayId, {
      method: 'DELETE'
    }).then(response => {
      if (!response.ok) {
        console.log('Could not delete birthday' + response);
      }
    });
  }
}
