<template>
  <section>
    <header>
      <h1>Birthdays app</h1>
    </header>

    <div id="addBday">
      <h2>Add new birthday</h2>
      <new-birthday @add-birthday="addBirthday"></new-birthday>
    </div>

    <div id="listBdays">
      <h2>All birthdays</h2>
      <table>
        <birthday
          v-for="birthday in birthdays"
          :key="birthday.id"
          :id="birthday.id"
          :name="birthday.name"
          :year="birthday.year"
          :month="birthday.month"
          :day="birthday.day"
          @delete="deleteBirthday"
        ></birthday>
      </table>
    </div>
  </section>
</template>

<script>
export default {
  created() {
    this.loadBdaysFromBackend();
  },
  data() {
    return {
      baseUrl: 'http://localhost:8080/',
      birthdays: []
    };
  },
  methods: {
    loadBdaysFromBackend() {
      // todo: add pagination / scrolling

      fetch(this.baseUrl + 'bdays/list', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          limit: 100
        })
      })
        .then(response => {
          if (response.ok) {
            return response.json();
          }
        })
        .then(data => {
          for (const i in data) {
            this.birthdays.push(data[i]);
          }
        });
    },

    addBirthday(name, day, month, year) {
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
        .then(bday => {
          this.birthdays.push(bday);
        });
    },

    deleteBirthday(id) {
      fetch(this.baseUrl + 'bday/' + id, {
        method: 'DELETE'
      }).then(response => {
        if (!response.ok) {
          console.log('Could not delete birthday' + response);
        } else {
          this.birthdays = this.birthdays.filter(
            birthday => birthday.id !== id
          );
        }
      });
    }
  }
};
</script>

<style>
* {
  box-sizing: border-box;
}
html {
  font-family: 'Jost', sans-serif;
}
body {
  margin: 0;
}
header {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.26);
  border-radius: 0px;
  padding: 1rem;
  background-color: #430058;
  color: white;
  text-align: center;
  width: 100%;
}
#app ul {
  margin: 0;
  padding: 0;
  list-style: none;
}
#app li,
#app form {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.26);
  margin: 1rem auto;
  border-radius: 10px;
  padding: 1rem;
  text-align: center;
  width: 90%;
  max-width: 40rem;
}
#app h2 {
  font-size: 1rem;
  border-bottom: 4px solid #ccc;
  color: #58004d;
  margin: 0 0 1rem 0;
}
#app button {
  font: inherit;
  cursor: pointer;
  border: 1px solid #430058;
  background-color: #430058;
  color: white;
  padding: 0.05rem 1rem;
  box-shadow: 1px 1px 2px rgba(0, 0, 0, 0.26);
}
#app button:hover,
#app button:active {
  background-color: #875e94;
  border-color: #430058;
  box-shadow: 1px 1px 4px rgba(0, 0, 0, 0.26);
}
#app input {
  font: inherit;
  padding: 0.15rem;
}
#app label {
  font-weight: bold;
  margin-right: 1rem;
  width: 7rem;
  display: inline-block;
}
#app form div {
  margin: 0.7rem 0;
}
</style>

