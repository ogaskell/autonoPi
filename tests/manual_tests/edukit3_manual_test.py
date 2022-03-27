import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

import examples.edukit3 as ek3  # noqa: E402

m = ek3.EduKit3Manager(vis=True)
m.motion.pol = [True, True]
m.mainloop()
