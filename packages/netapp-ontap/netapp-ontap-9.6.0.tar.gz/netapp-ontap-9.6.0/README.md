# NetApp ONTAP
The Python client library is a package you can use when writing scripts to access the
ONTAP REST API. It provides support for several underlying services, including connection
management, asynchronous request processing, and exception handling. By using the Python
client library, you can quickly develop robust code to support the automation of your ONTAP
deployments.

# Getting started

## Software requirements
Before installing the Python client library, you must make sure the following packages are
installed on your system:
```
1. python 3.5 or later
2. requests 2.21.0 or later
3. marshmallow between 3.0.0rc5 and 3.0.0rc7
```

## Installing and importing the package
You must install the package using the pip utility:

```
pip install netapp-ontap
```

After installing the package, you can import the objects you need into your application:

```python
from netapp_ontap.resources import Volume, Snapshot
```

## Creating an object

You can create an object in several different ways. Here are three examples of
creating an equivalent `netapp_ontap.resources.volume` object.

```python
from netapp_ontap.resources import Volume

# Example 1 - keyword arguments
volume = Volume(name='vol1', svm={'name': 'vs1'}, aggregates=[{'name': 'aggr1'}])

# Example 2 - dict as keyword arguments
data = {
    'name': 'vol1',
    'svm': {'name': 'vs1'},
    'aggregates': [{'name': 'aggr1'}],
}
volume = Volume(**data)

# Example 3 - using the from_dict() method
volume = Volume.from_dict({
    'name': 'vol1',
    'svm': {'name': 'vs1'},
    'aggregates': [{'name': 'aggr1'}],
})
```

## Performing actions on an object

After you create an object, you can perform actions on the object based
on the purpose and design of your application. The example below illustrates
how to create a new volume and then take a snapshot.

Note that when using the library, in all cases you must first establish a
connection to the management LIF of the ONTAP system using the
`netapp_ontap.host_connection.HostConnection` object. In the example below,
the connection is created and then set as the global default.
This means that all objects and the associated actions reuse
this same connection. See *Host connections* for more information.

```python
from netapp_ontap import config
from netapp_ontap.host_connection import HostConnection
from netapp_ontap.resources import Volume, Snapshot

config.CONNECTION = HostConnection('myhost.mycompany.com', 'username', 'password')

volume = Volume(name='vol1', svm={'name': 'vs1'}, aggregates=[{'name': 'aggr1'}])
volume.post()
snapshot = Snapshot.from_dict({
    'name': '%s_snapshot' % volume.name,
    'comment': 'A snapshot of %s' % volume.name,
    'volume': volume.to_dict(),
})
snapshot.post()
```

# Additional considerations

In most cases, the objects and actions in the library can be mapped directly
to equivalent cURL commands run against the ONTAP REST interface. However, there are a few
exceptions you should be aware of.

## Property names

If a property of a resource is named the same as one of the Python reserved names,
the name will be transposed when accessing the member of the resource. For example,
if there is a resource named "Foo" that has a property defined in the API named "class",
the property name would instead be "class_" when using the library. For example:

```python
from netapp_ontap.resources import Foo

foo = Foo()
foo.class_ = "high"
```

# Documentation
To view the full documentation, visit https://library.netapp.com/ecmdocs/ECMLP2858435/html/index.html
or to view an offline copy, see the `<python_environment>/lib/<python_version>/site_packages/netapp_ontap/docs`
Documentation of ONTAP's REST APIs and other helpful resources can be found at https://devnet.netapp.com/restapi.

# Compatibility

The version assigned to the library consists of the major ONTAP release it is generated
from and a minor version for the library within that release. The minor version allows the
library to be updated within the same ONTAP release. For example, valid versions for
the library associated with ONTAP 9.6 include 9.6.1, 9.6.2, and so on.

Client libraries that have the same major version as ONTAP are completely compatible.
For example, the libraries netapp-ontap-9.6.1 and netapp-ontap-9.6.4 are fully
compatible with both ONTAP 9.6 and ONTAP 9.6P1.

A client library with a major version that does not match the ONTAP release can still be
used, however it will not be fully compatible with the REST API. For example, the library
netapp-ontap-9.6.4 is only partially compatible with ONTAP 9.7. In these cases, the
library may encounter unknown fields or APIs. When this occurs, the library will ignore
unknown fields, return an error, or raise a runtime exception.

# Copyright, trademarks, and feedback
## Copyright information
Copyright &copy; 2019 NetApp, Inc. All Rights Reserved. Printed in the U.S.

No part of this document covered by copyright may be reproduced in any form or by any means&#8208;graphic,
electronic, or mechanical, including photocopying, recording, taping, or storage in an electronic
retrieval system&#8208;without prior written permission of the copyright owner.

Software derived from copyrighted NetApp material is subject to the following license
and disclaimer:

THIS SOFTWARE IS PROVIDED BY NETAPP "AS IS" AND WITHOUT ANY EXPRESS OR IMPLIED WARRANTIES,
INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
PARTICULAR PURPOSE, WHICH ARE HEREBY DISCLAIMED. IN NO EVENT SHALL NETAPP BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)ARISING IN
ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

NetApp reserves the right to change any products described herein at any time, and without notice.
NetApp assumes no responsibility or liability arising from the use of products described herein,
except as expressly agreed to in writing by NetApp. The use or purchase of this product does not
convey a license under any patent rights, trademark rights, or any other intellectual property
rights of NetApp. The product described in this manual may be protected by one or more U.S.
patents, foreign patents, or pending applications.

RESTRICTED RIGHTS LEGEND: Use, duplication,or disclosure by the government is subject to
restrictions as set forth in subparagraph (c)(1)(ii) of the Rights in Technical Data and
Computer Software clause at DFARS 252.277-7103 (October 1988) and FAR 52-227-19 (June 1987).

## Trademark information
NETAPP, the NETAPP logo, and the marks listed on the NetApp Trademarks page are trademarks of
NetApp, Inc. Other company and product names may be trademarks of their respective owners.
http://www.netapp.com/us/legal/netapptmlist.aspx

## Feedback
You can help us to improve the quality of our documentation by sending us your feedback.
If you have suggestions for improving this document, send us your comments by email.

<doccomments@netapp.com>

To help us direct your comments to the correct division, include in the subject line
the product name, version, and operating system.

If you want to be notified automatically when production-level documentation is released
or important changes are made to existing production-level documents,
follow Twitter account @NetAppDoc.

You can also contact us in the following ways:

NetApp, Inc., 1395 Crossman Ave, Sunnyvale, CA 94089 U.S.

Telephone: +1 (408) 822-6000

Fax: +1 (408) 822-4501

Support telephone: +1 (888) 463-8277
