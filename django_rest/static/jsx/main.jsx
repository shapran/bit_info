var React = require('react');
var ReactDOM = require('react-dom');
var PropTypes = require('prop-types');

import axios from 'axios';


var Dropdown;
var Dropdown = React.createClass({

  getCookie: function (name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(
                    cookie.substring(name.length + 1)
                );
                break;
            }
        }
    }
    return cookieValue;
  },

  getInitialState: function () {
    return { info: [{name: 'bob', symbol: 'great'}] };
  },

  componentDidMount: function () {
    var csrf_token = this.getCookie('csrftoken');

        var config = {
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'X-CSRF-Token': csrf_token
            }
        };

        var base_url = 'http://127.0.0.1:8000/api/v1/symbols/?page=';
        var data = [];
        var total_pages = 1;

        axios.get(base_url + total_pages, config).then(function (res) {
            total_pages = res.data.total_pages;

            var promises = [];
            for (var i = 1; i <= 1; i++) {
                promises.push(axios.get(base_url + i, config))
            }
            axios.all(promises).then(function (results) {
                results.forEach(function (response) {
                    // data.push.apply(data, response.data.results);
                    data.push(response.data.results[0]);
                })
            });
        });
        console.log('data', data);
        this.setState({info: data});
    },

  render: function() {

    console.log('fet',this.state.info);
    var symbols = this.state.info.map(function (symbol) {
            console.log('inner',  symbol);
    });

    console.log(symbols);
    return (
      <select>{symbols}</select>
    );
  }
});

ReactDOM.render(
        <Dropdown id='myDropdown'/>,
        document.getElementById('example'));