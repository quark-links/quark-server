/*
 *     This file is part of VH7.
 *
 *     VH7 is free software: you can redistribute it and/or modify
 *     it under the terms of the GNU General Public License as published by
 *     the Free Software Foundation, either version 3 of the License, or
 *     (at your option) any later version.
 *
 *     VH7 is distributed in the hope that it will be useful,
 *     but WITHOUT ANY WARRANTY; without even the implied warranty of
 *     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *     GNU General Public License for more details.
 *
 *     You should have received a copy of the GNU General Public License
 *     along with VH7.  If not, see <https://www.gnu.org/licenses/>.
 */

package uk.vh7.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.servlet.view.RedirectView;
import uk.vh7.exception.ShortLinkNotFoundException;
import uk.vh7.model.ShortLink;
import uk.vh7.service.ShortLinkService;

import java.util.Optional;

@Controller
public class RedirectController {
    private final ShortLinkService shortLinkService;

    public RedirectController(ShortLinkService shortLinkService) {
        this.shortLinkService = shortLinkService;
    }

    @GetMapping("/{alphaId}")
    public RedirectView shortLinkRedirect(@PathVariable String alphaId) {
        Optional<ShortLink> shortLink = shortLinkService.findByAlphaId(alphaId);
        if (!shortLink.isPresent()) {
            throw new ShortLinkNotFoundException(alphaId);
        }

        RedirectView redirectView = new RedirectView();
        redirectView.setUrl(shortLink.get().getLongUrl());
        return redirectView;
    }
}
