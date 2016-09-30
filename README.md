# OpenDash
### The configurable alternative to Amazon Dash

Hi! OpenDash is all about bringing Internet and real life closer together, much like Amazon Dash but more configurable and with less data mining.

## Summary
To make it simple, OpenDash consists of two parts:
A number of hardware buttons called 'DashAgents', which are communicating with a base-station called 'DashControl'.

### What the heck are 'DashAgents'?
The hardware buttons are called DashAgents. They consist of a tiny Arduino-compatible SOC that is capable of communicating using Bluetooth LE and a battery adapter using two AAA-cells as well as a button. The casing can really be anything, however a reusable housing design will be provided as 3D model at some date, which can for example 3D printed.

### And what about the 'DashControl' base-station?
The base-station can be any micro-computer or SOC capable of bluetooth, internet and python - I'm developing it using a Raspberry Pi 3. It runs the scripts contained currently in this repository.

## What is all this for?
It can really do anything. The idea however is the following:
Imagine you know you need cat food, toilet paper or some beverage on a weekly or monthly basis. You want to order it online (for some reason). You don't want to log in to that particular online shop every week or month and order the same thing by hand - or maybe its actually six different things from six different online shops.

### Automatically order cat food... or anything!
So here comes OpenDash! You place a DashAgent near your cat food/whatever storage and turn it on. The DashControl will pair automatically with the device. You open the OpenDashDashboard (name pending!) on any device in your local network and add the 'AwesomeShop OpenDash Connector' plugin. You then add your AwesomeShop user credentials inside the plugin settings.

Next you create an 'action'. It contains, for example the directive: 'Buy product with <SKU> from <AwesomeShop>'. You save it and assign it to your DashAgent. The system and plugin resolve the directive/s in the action to functions that are simulating a mouse, clicking the right buttons on the webpage of "AwesomeShop" to buy the product you want.

#### How complex can such a directive or action get?
Well, in theory there is no hard limit. An action may well contain dozens of directives, assume the following example:
'Buy products with <List_of_SKUs> from <AwesomeShop>'
'Buy product with <SKU> from <AnotherShop>'
'Buy product with <SKU> from <Amazon>'
and so on.

The possible complexity of a directive itself is highly dependent on the plugin for the webpage you want to automate. Amazon is comparatively easy because it allows 'OneClick' orders, once you are signed in and found the right product. This may well change when the development reaches this point.

### So what happens when I press the button?
The DashAgents each have a unique MAC address, like every Bluetooth device. It is sent to the DashControl base-station when you press the button. The base-station has a action registered for that MAC address, which is run if the address is received via Bluetooth.

The action itself could be ordering a product off Amazon.
This consists of several subtasks, most done by external third party frameworks 'Moccha' & 'Webdriver.io'. They interact with a webpage by simulating clicks on given elements of the page. The plugin system in DashControl consists of function packages / script files which contain high level wrappers for these 'click' functions to make communicating easy.

Since this way it 'simulates' a real human user, it can do most thigs you could do on a webpage (within certain limits).

#### Won't I need to replace the batteries constantly?
Nope. Calculations have shown that a 'DashAgent' should run half a year off those two AAA-batteries, if used once a week. More accurate test results will be available when a final prototype is assembled.

## So why not just use AmazonDash buttons, they are cheaper and look better too...
This project is not intended as a ready made system to just plug-in and use - however it can be.

I like the basic idea of Amazon Dash, just don't like the details of it. It seems limited and I can never be too sure what data is collected and what is done with it.
Also this is a open project, for the sake of fun and learning something. I wanted a custom hackable solution just like Amazon Dash - but with all possibilities open. Trough the plugin system, you could let OpenDash toggle your lights, control your vacuum robot etc.
