**Page 156**

Complete the content of the paragraph elements based on the image below. To display words in bold (`bold`), use the appropriate tag. Save the file and check the result in the browser.

![Book image](../images/p162-01.png)

To fix the mobile view, remove the class `w-75` from the `article` element and add the related style to the file `styles.css`:

![Book image](../images/p162-02.png)

For devices with a width less than 600 pixels, add the following rule to the file `styles.css`:

![Book image](../images/p162-03.png)

### Learn more

Designing a toolbar that contains a logo, a search box, Sign in | Register options, and a shopping cart In this workshop you will create an area similar to the image below above the menu bar:

![Book image](../images/p162-04.png)

Create a logo with a height of 70 pixels and then save the image file with the name `logo.jpg` in the site’s `images` folder.

A search icon should appear inside the search box. To download a search icon, use the site `svgrepo.com` and search for the word `search` on it. Adjust your preferred icon with the `Edit` `vector` button at the smallest size and preferred color, then click the `Export` button. Save the icon file with the name `search.svg` in the site’s images folder (`images`).


---

**Page 157**

The image on the previous page contains a logo, a search box (including a search icon and a text box), a Sign in | Register option, and a shopping cart. Add these elements as shown below to the page `index.html` before the `nav` element:

![Book image](../images/p163-01.png)

Set the styles of the elements in the desktop view as follows:

![Book image](../images/p163-02.png)

Add the following classes to the `toolbar` element. Then save the file and check the result in the browser.

![Book image](../images/p163-03.png)


---

**Page 158**

With the `CSS` settings above, the “Sign in|Register” option and the logo are removed from the mobile view, so these options must be displayed somewhere else. It is better to display these options as a fixed layer at the bottom of the page. For this purpose, enter the following code before `<main/>`:

![Book image](../images/p164-01.png)

The class `fixed-bottom` keeps the `bottom-toolbar` layer fixed at the bottom of the page.

Write the following style for the `bottom-toolbar` element:

![Book image](../images/p164-02.png)

Add the following style for correct display of the toolbar in the mobile view:

![Book image](../images/p164-03.png)

With these settings, the `bottom-toolbar` element appears at the bottom of the mobile device as shown below.

![Book image](../images/p164-04.png)

To create space between the menu and the `toolbar`, use the class `mt-3` on the `<nav>` tag.

Because the Sign in|Register and shopping cart options have been added to the `toolbar` section, remove the `user-actions` element from the navigation menu (the `top-menu` element). Then remove the related styles from the file `styles.css`. With the `user-action` area removed, the flex properties in the `.top-menu` class are no longer needed. So remove the flex properties as well. In the end, what remains inside the `top-menu` class will be the `max-width` property.

![Book image](../images/p164-05.png)


---

**Page 159**

It is better for the menu options to be distributed horizontally in the center of the page; for this, use the class `-justify` `content-center` on the `ul` element:

![Book image](../images/p165-01.png)

With the code above, all properties of the selector `.top-menu` `ul` were replaced with equivalent Bootstrap classes. Therefore, remove the properties inside the selector `.top-menu` `ul` from the file `styles.css`.

With the settings above, the following result is expected:

![Book image](../images/p165-02.png)

Customizing Bootstrap classes Bootstrap classes have predefined properties and values that make it possible to design page elements quickly. Sometimes it is necessary for the page developer to change how these classes work.

This can be done with `CSS` and `SASS`1. To change the style of a class with `CSS`, the property of the desired class must be set with new values. By default, applying a Bootstrap class has higher priority. Therefore, to raise the importance of the custom class you must use the word `important` ! at the end of the new value; otherwise the new value is not applied.

Changing the style of a Bootstrap color class

### Workshop

In this workshop you will change the color of the class `bg-light` in the file `index.html`. For this purpose, write the following style for the class `bg-light` as shown below:

![Book image](../images/p165-03.png)

Attaching the file `styles.css` must be done after attaching the file `bootstrap.min.css`; otherwise the default Bootstrap class settings will have execution priority. The class `bg-light` is used on two elements: the search box and `article`. After saving the code above, check whether the color change has been applied to these two elements.

1 A tool that makes writing, organizing, and maintaining `CSS` code in web projects simpler and more professional.


---
