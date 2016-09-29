(function ($) {
  $.fn.toggleAttr = function (attribute, value) {
    if (attribute && value) {
      console.log('attribute and value was given')
      if ($(this).attr(attribute)) {
        console.log('element already has \''+attribute+'\', removing it.')
        $(this).removeAttr(attribute)
      } else {
        console.log('element does not have \''+attribute+'\'.')
        if (value) {
          $(this).attr(attribute, value)
          console.log('additional value given, adding attribute with value.')
        } else {
          $(this).attr(attribute)
          console.log('adding attribute.')
        }
      }
    }
  }

  var agent_list = '.agent-container ul'
  var agent_panel = '#dashboard-agents'
  var scan_button = 'button.scan-button'

  function toggleAnimateScanButton () {
    jQuery(scan_button+' .glyphicon').toggleClass('rotate')
    jQuery(scan_button).toggleClass('btn-default btn-warning').attr('disabled', 'disabled')
  }

  jQuery(agent_panel).find(scan_button).on('click', function () {
    toggleAnimateScanButton()
    jQuery(agent_list).load('/dashboard/get_agents', function () {
      toggleAnimateScanButton()
    })
  })
}(jQuery))
