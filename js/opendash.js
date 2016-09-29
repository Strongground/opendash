(function ($) {
  $.fn.toggleAttr = function (attribute, value) {
    value = value || ''
    if (attribute.length > 0) {
      if (($(this).attr(attribute) != undefined) && ($(this).attr(attribute) != value)) {
          window.alert('element already has \''+attribute+'\', removing it.')
          $(this).removeAttr(attribute)
      } else if ($(this).attr(attribute) == value) {
          window.alert('element already has \''+attribute+'\' with value \''+value+'\', toggling value instead.')
          value = ''
          $(this).attr(attribute, value)
      } else {
        window.alert('element does not yet have \''+attribute+'\'. creating it.')
        $(this).attr(attribute, value)
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
