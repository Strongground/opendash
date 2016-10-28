# OpenDash
### The configurable alternative to Amazon Dash

Hi! OpenDash is all about bringing Internet and real life closer together, much like Amazon Dash but more configurable and with less data mining.

## Summary
To make it simple, OpenDash consists of two parts:
A number of hardware buttons called 'DashAgents', which are communicating with a base-station called 'DashControl'.

### What the heck are 'DashAgents'?
The hardware buttons are called DashAgents. They consist of a tiny Arduino-compatible SOC that is capable of communicating using Bluetooth LE and a battery adapter using two AAA-cells as well as a button. The casing can really be anything, however a reusable housing design will be provided as 3D model at some date, which can for example 3D printed. A part list will be published as well.

### And what about the 'DashControl' base-station?
The base-station can be any micro-computer or SOC capable of bluetooth, internet and python - I'm developing it using a Raspberry Pi 3. It runs the scripts contained currently in this repository.

## What is all this for?
It can really do anything. The idea however is the following:
Imagine you know you need cat food, toilet paper or some beverage on a weekly or monthly basis. You want to order it online (for some reason). You don't want to log in to that particular online shop every week or month and order the same thing by hand - or maybe its actually six different things from six different online shops.

### Automatically order cat food... or anything!
So here comes OpenDash! You place a DashAgent near your cat food/whatever storage and turn it on. You open the OpenDashDashboard (name pending!) web based control panel on any device with a web browser connected to your local network. The DashControl will pair automatically with the device once you hit the "Find Agents" button. Then you add the 'AwesomeShop OpenDash Connector' plugin. Also add your AwesomeShop user credentials inside the plugin settings.

Next you create an 'Action'. It contains, for example the directive: 'Buy product from <URL> from <AwesomeShop>'. You save it and assign it to your DashAgent.
Internally, the system resolves your directive/s in the newly created 'Action' to calls of wrapper functions that are simulating a mouse, clicking the right buttons on the webpage of "AwesomeShop" to buy the product you want with the user login you provided earlier. It's basically doing the same things you'd do when shopping, only with less distraction (and also faster).

#### How complex can such a directive or action get?
Well, in theory there is no hard limit. An action may well contain dozens of directives, assume the following example:
'Buy products from <List_Of_URLs> from <AwesomeShop>'
'Buy product from <URL> from <AnotherShop>'
'Buy product from <URL> from <Amazon>'
and so on.

The possible complexity of a directive itself is highly dependent on the plugin for the webpage you want to automate. Amazon is comparatively easy because it allows 'OneClick' orders, once you are signed in and found the right product.

### So what happens when I press the button?
The DashAgents each have a unique MAC address, like every Bluetooth device. It is sent to the DashControl base-station when you press the button. The base-station has a 'Action' registered for that MAC address, which is consequently run. You receive the order confirmation and shipping mails as usual and the finally your product/s.

Maybe later

The action itself could be ordering a product off Amazon.
This consists of several subtasks, most done by external third party framework 'Selenium' and the corresponding python-wrappers. They interact with a webpage by simulating clicks on given elements of the page. The plugin system in DashControl consists of function packages / script files which contain high level wrappers for these 'click' functions to make communicating easy.

Since this way it 'simulates' a real human user, it can do most things you could do on a webpage (within certain limits).

#### Won't I need to replace the batteries constantly?
Well, they won't last forever, yes. But calculations have shown that a 'DashAgent' should run half a year off those two AAA-batteries, if used once a week. More accurate test results will be available when a prototype is assembled.

## So why not just use AmazonDash buttons, they are cheaper and look better too...
This project is not intended as a ready made system to just plug-in and use - however it can be.

I like the basic idea of Amazon Dash, but not some details. It seems limited and I can never be too sure what data is collected and what is done with it.
Also this is an open project, for the sake of fun and learning something. I wanted a custom hackable solution just like Amazon Dash - but with all possibilities open. Trough the plugin system, you can basically let the button do anything while DashControl should aim to deliver an easy way to map actions with real life control elements in your surrounding.
