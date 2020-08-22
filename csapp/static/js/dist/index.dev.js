"use strict";

var addItem = function addItem() {
  var container = document.getElementById('container');
  var input = document.createElement('input');
  input.setAttribute('type', 'text');
  input.setAttribute('name', 'label');
  input.setAttribute('id', 'label');
  var submit = document.createElement('input');
  submit.setAttribute('type', 'submit');
  submit.setAttribute('value', 'Add item');
  submit.setAttribute('class', 'submit-btn');
  var form = document.createElement('FORM');
  form.setAttribute('action', '/');
  form.setAttribute('method', 'POST');
  form.appendChild(input);
  form.appendChild(submit);
  var a = document.createElement('a');
  a.appendChild(form);
  var numberItems = container.children.length;
  container.insertBefore(a, container.children[numberItems - 1]);
};