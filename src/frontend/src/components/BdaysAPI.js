export class BdaysAPI {
  constructor(baseUrl) {
    this.baseUrl = baseUrl;
  }

  listAll() {
    // todo: add pagination

    fetch(this.baseUrl + 'bdays/list')
      .then(response => {
        if (response.ok) {
          return response.json();
        }
      })
      .then(data => {
        var bdays = [];
        for (const i in data) {
          bdays.push(data[i]);
        }
        return bdays;
      });

  }

  add(name, day, month, year) {
    var newBday = null;
    fetch(this.baseUrl + 'bday', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        name: name,
        year: year,
        month: month,
        day: day
      })
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
