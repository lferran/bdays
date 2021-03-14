<template>
  <section>
    <header>
      <h1>Birthdays app</h1>
    </header>

    <div class="container">
      <div class="side-container">
        <div class="addbday">
          <h2>Add new birthday</h2>
          <new-birthday @add-birthday="addBirthday"></new-birthday>
        </div>
      </div>

      <div class="bdayslist">
        <h2>All birthdays</h2>
        <table>
          <tbody>
            <birthday
              v-for="birthday in visibleBirthdays"
              :key="birthday.id"
              :id="birthday.id"
              :name="birthday.name"
              :year="birthday.year"
              :month="birthday.month"
              :day="birthday.day"
              @delete="deleteBirthday"
            ></birthday>
          </tbody>
        </table>
        <div class="searchbar">
          <input class="searchinput" @keyup="updateSearchTerm" type="text" placeholder="Search.." />
        </div>
      </div>
    </div>
  </section>
</template>

<script>
function sortByName(array) {
  return array.sort((a, b) => (a.name > b.name ? 1 : -1));
}

export default {
  created() {
    this.loadBdaysFromBackend();
  },
  data() {
    return {
      baseUrl: 'http://localhost:8080/',
      allBirthdays: [],
      enteredSearchTerm: ''
    };
  },
  computed: {
    visibleBirthdays: function() {
      var bdays = [];
      if (this.enteredSearchTerm == '') {
        bdays = this.allBirthdays;
      } else {
        bdays = this.allBirthdays.filter(birthday =>
          birthday.name
            .toLowerCase()
            .includes(this.enteredSearchTerm.toLowerCase())
        );
      }
      return sortByName(bdays);
    }
  },
  methods: {
    updateSearchTerm(event) {
      this.enteredSearchTerm = event.srcElement.value;
    },
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
            this.allBirthdays.push(data[i]);
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
          this.allBirthdays.push(bday);
        });
    },

    deleteBirthday(id) {
      fetch(this.baseUrl + 'bday/' + id, {
        method: 'DELETE'
      }).then(response => {
        if (!response.ok) {
          console.log('Could not delete birthday' + response);
        } else {
          this.allBirthdays = this.allBirthdays.filter(
            birthday => birthday.id !== id
          );
        }
      });
    }
  }
};
</script>

<style>
/* Header */

html {
  font-family: 'Courier New', monospace;
}

header {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.26);
  padding: 1rem;
  background-color: #fed049;
  color: #282846;
  text-align: left;
  width: 100%;
}

h1 {
  font-size: 2em;
}

body,
html {
  margin: 0;
}

.container {
  display: inline-flex;
  flex-direction: row;
  flex-wrap: wrap;
  justify-content: flex-start;
  color: #007580;
  background-color: #d8ebe4;
  width: 100%;
  height: 1000px;
  align-items: baseline;
}

.side-container {
  width: 200px;
  height: 20px;
  margin-right: 40px;
}

input, button {
  background-color:#f5f5f5;
}

.addbday {
  padding: 1em;
}

.addbday label {
  padding: 5px;
}

.addbday button {
  margin-left: 5px;
  margin-top: 10px;
}

.bdayslist {
  width: 80%;
}

td {
  padding: 0 20px;
}

tr:hover {background-color:#f5f5f5;}

thead,
tbody {
  display: block;
}

tbody {
  max-height: 200px;
  overflow-y: auto;
  overflow-x: hidden;
}

.searchinput {
  margin-top: 10px;
  margin-left: 10px;
}

</style>
