
const TailboneDatepicker = {

    template: [
        '<b-datepicker',
        'placeholder="Click to select ..."',
        `:name="name"`,
        `:id="id"`,
        'editable',
        'icon-pack="fas"',
        'icon="calendar-alt"',
        ':date-formatter="formatDate"',
        ':date-parser="parseDate"',
        ':value="value ? parseDate(value) : null"',
        '@input="dateChanged"',
        '>',
        '</b-datepicker>'
    ].join(' '),

    props: {
        name: String,
        id: String,
        value: String
    },

    methods: {

        formatDate(date) {
            // just need to convert to simple ISO date format here, seems
            // like there should be a more obvious way to do that?
            var year = date.getFullYear()
            var month = date.getMonth() + 1
            var day = date.getDate()
            month = month < 10 ? '0' + month : month
            day = day < 10 ? '0' + day : day
            return year + '-' + month + '-' + day
        },

        parseDate(date) {
            // note, this assumes classic YYYY-MM-DD (i.e. ISO?) format
            var parts = date.split('-')
            return new Date(parts[0], parseInt(parts[1]) - 1, parts[2])
        },

        dateChanged(date) {
            this.$emit('input', this.formatDate(date))
        }
    }

}

Vue.component('tailbone-datepicker', TailboneDatepicker)
