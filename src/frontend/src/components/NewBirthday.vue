<template>
  <form @submit.prevent="submitData">
    <div>
      <label>Name</label>
      <input type="text" v-model="enteredName" />
    </div>
    <br>
    <div>
      <label>Date of birth</label>
      <input type="date" v-model="enteredDate" />
    </div>
    <div>
      <button>Submit</button>
    </div>
  </form>
</template>

<script>
export default {
  emits: ['add-birthday'],
  data() {
    return {
      enteredName: '',
      enteredDate: ''
    };
  },
  methods: {
    submitData() {
      const theDate = new Date(this.enteredDate);
      this.$emit(
        'add-birthday',
        this.enteredName,
        theDate.getDate(),
        theDate.getMonth() + 1,
        theDate.getFullYear()
      );
    }
  }
};
</script>
