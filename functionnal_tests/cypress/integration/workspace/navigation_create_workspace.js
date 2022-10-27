describe('navigate :: create_new > workspace', function () {
  before(() => {
    cy.resetDB()
    cy.setupBaseDB()
  })

  beforeEach(function () {
    cy.loginAs('administrators')
    cy.visit('/ui/workspaces/1/dashboard')
  })
  it('', function () {
    cy.get('[data-cy=sidebarCreateSpaceBtn]')
      .should('be.visible')
      .click()
    cy.get('.cardPopup__container .cardPopup__header__title')
      .should('be.visible')
    cy.get('.cardPopup__container .newSpace__button .btn')
      .should('be.visible')
      .and('be.disabled')
    cy.get('.cardPopup__container .newSpace__input')
      .type('Space name')
      .should('have.attr', 'value', 'Space name')
      .and('have.attr', 'placeholder')
    cy.get('.cardPopup__container .singleChoiceList')
      .should('be.visible')
    cy.get('.cardPopup__container .singleChoiceList__item')
      .should('have.length', 3)
      .last()
      .click()
    cy.get('.cardPopup__container .newSpace__button .btn')
      .should('be.visible')
      .and('be.enabled')
      .click()
    cy.get('div.newSpace__input')
      .should('be.visible')
    cy.get('.newSpace__button .btn').last()
      .should('be.visible')
      .and('be.disabled')
    cy.get('.cardPopup__container .singleChoiceList')
      .should('be.visible')
    cy.get('.cardPopup__container .singleChoiceList__item')
      .and('have.length', 4)
      .last()
      .click()
    cy.get('.newSpace__button .btn')
      .last()
      .should('be.visible')
      .and('be.enabled')
    cy.get('.newSpace__button .btn')
      .first()
      .should('be.visible')
      .click()
    cy.get('.cardPopup__container .newSpace__input')
      .should('be.visible')
      .and('have.attr', 'value', 'Space name')
    cy.get('.cardPopup__container .cardPopup__header__close button')
      .should('be.visible')
      .click()
    cy.get('.cardPopup__container .cardPopup__header__title')
      .should('not.be.visible')
  })
})
