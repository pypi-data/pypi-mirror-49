define([
  'base/js/namespace',
  'base/js/utils',
  'base/js/events'
], function(Jupyter, utils, events) {
  function load_ipython_extension() {
    function publish() {
      events.off('notebook_saved.Notebook', publish)
      var version =  prompt('버전명을 입력하세요')
      if (!version) {
        return;
      }
      utils.ajax({
        url: '/publish_notebook',
        type: 'POST',
        dataType: 'json',
        data: JSON.stringify({
          version: version,
          nb_path: Jupyter.notebook.notebook_path
        })
      }).done(function(data) {
        console.debug(data);
        alert('publish done : ' + data.uploaded);

      }).fail(function(xhr) {
        console.debug(xhr);
        if (xhr.status === 409) {
          alert('version is exists');
        }
      });
    }

    var handler = function () {
      console.log(Jupyter)
      events.on('notebook_saved.Notebook', publish)
      Jupyter.notebook.save_checkpoint();
    };

    var action = {
      icon: 'fa-book', // a font-awesome class used on buttons, etc
      help    : 'publish notebook',
      help_index : 'zz',
      handler : handler
    };
    var prefix = 'jupyter_extension_publish';
    var action_name = 'publish_notebook';

    var full_action_name = Jupyter.actions.register(action, action_name, prefix);
    Jupyter.toolbar.add_buttons_group([full_action_name]);
  }

  return {
    load_ipython_extension: load_ipython_extension
  };
});
