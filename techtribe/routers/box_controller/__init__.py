# SPDX-FileCopyrightText: 2023 
#
# SPDX-License-Identifier: MPL-2.0


from fastapi import APIRouter
from techtribe.routers.box_controller import web, embedded

router = APIRouter()

router.include_router(web.router, prefix="/web")
router.include_router(embedded.router, prefix="/embedded")
