% setdefault('title', 'Welcome to OpenDash!')

<html lang="en"><head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta name="description" content="">
    <meta name="author" content="">
    <link rel="icon" href="/images/favicon.ico">

    <title>{{title}}</title>

    <!-- Core CSS -->
    <link href="/css/bootstrap.css" rel="stylesheet">
    <link href="/css/opendash.css" rel="stylesheet">
  </head>

  <body>
    % if showMenu:
    %   include('menubar.tpl')
    % end

    <div class="container">
